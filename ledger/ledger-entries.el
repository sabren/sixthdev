
; This is a refactoring of ledger-iterate-entries from John Weigly's ledger.el
; ( http://github.com/jwiegley/ledger/tree/master/lisp/ledger.el#L150 )

;; LICENSE: this code inherits the GPL from ledger.el
;;
;; This is free software; you can redistribute it and/or modify it under
;; the terms of the GNU General Public License as published by the Free
;; Software Foundation; either version 2, or (at your option) any later
;; version.


(require 'ledger)

; crappy global variable.
; i wasn't sure where to put this after the refactoring.
(defvar current-year)
(setq current-year (nth 5 (decode-time (current-time))))

; surely there's an emacs primitive for these two
; but darned if I can find them

(defun for-lines-from-point (command) 
  (while (not (eobp))
    (funcall command)
    (forward-line)))

(defun for-lines-in-buffer (command)
  (goto-char (point-min))
  (for-lines-from-point command))


(defun at-start-of-ledger-entry ()
  ; @TODO: clarify this regexp!!!
  (looking-at (concat "\\(Y\\s-+\\([0-9]+\\)\\|"
		      "\\([0-9]\\{4\\}+\\)?[./]?"
		      "\\([0-9]+\\)[./]\\([0-9]+\\)\\s-+"
		      "\\(\\*\\s-+\\)?\\(.+\\)\\)")))

; returns either () or '(start date mark entry-description)   
(defun ledger-parse-entry-at-point ()
  ; we wind up testing this twice because of the assertion,
  ; but without it this function could be called any time,
  ; and the global match vars might break
  (if (at-start-of-ledger-entry)
      (let (maybe-year (match-string 3))
	(let ((start (match-beginning 0))
	      (year  (if (and maybe-year 
			      (> (length maybe-year) 0))
			 (string-to-number maybe-year)
		       current-year))
	      (month (string-to-number (match-string 4)))
	      (day (string-to-number (match-string 5)))
	      (mark (match-string 6))
	      (desc (match-string 7)))
	  
	  ; here's the global again... :/
	  (setq current-year year)

	  (list start (encode-time 0 0 0 day month year)
		mark desc)))
    nil))


; callback params: (start date mark entry-description)
; where start is the position in the buffer and mark is "*","!", or ""
(defun for-entry-in-ledger (callback)
  (for-lines-in-buffer 
   (lambda ()
     (when (at-start-of-ledger-entry)
       (apply callback (ledger-parse-entry-at-point))))))


; example:
; this puts an x in front of every ledger line in current buffer
; (completely pointless, except for testing)
; --------------------------------------------------------------
; (for-entry-in-ledger
;   (lambda (start date mark desc) 
;   (insert "x")))
