;
; reconcile.el  $Id$
;
; Author: michal j wallace (firstname.lastname@gmail.com)
; License: Do whatever you want with it (AT YOUR OWN RISK!)

(require 'ledger)
;-------------------------------------------------------
;
; This is (a start on) a new ledger reconciliation 
; program for emacs. 
;
; The idea is to open two frames side-by-side:
;
;  * Frame 1 contains your ledger.
;
;  * Frame 2 contains a ledger generated from your 
;    electronic bank statement. (see bofaconvert.py 
;    for an example conversion program)
;
; You work from the *bank* ledger, and press the following keys:
; (use M-x enable-reconcile-keys  first (work in progress, I know))
;
; NOTE: THESE KEYS ARE DESTRUCTIVE. *ONLY* USE THEM IN THE BANK's BUFFER!

(defun enable-reconcile-keys ()
  (interactive)
  (global-set-key [f4] 'first-bank-entry)
  (global-set-key [f5] 'find-next-ledger-match)
  (global-set-key [f6] 'accept-entry-match)
  (global-set-key [f7] 'move-and-accept-entry)
  (global-set-key [f8] 'move-bank-entry-to-ledger)

  ; this is mostly for debugging, and you actually can use this
  ; one in either buffer:
  (global-set-key [f12] 'goto-next-ledger-entry))
;
; Basically, you hit the first-bank-entry key to find the 
; first match (it's based on the payee string, NOT the amount)
;
; To see the next entry for that payee, hit the find-next-ledger-match
; button.
;
; Once you find the match, hit the accept-entry-match button.  This
; will insert an effective date, mark the transaction as cleared in
; your ledger, and remove it from the bank ledger.
;
; If there isn't a match, you can just cut and paste the bank entry to
; your ledger with move-bank-entry-to-ledger. It will automatically
; place the entry in the correct position in the file, based on the
; date (assuming, of course, that your entries are in chronological
; order to begin with).

; To check my work, I keep a terminal window open that constantly
; monitors the cleared balance:
;
;  watch ledger --cleared bal asset:checking
;
; This is very much a work in progress, and my first serious
; attempt at writing elisp code so feedback and patches welcome!

;-------------------------------------------------------

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
  ; @TODO: handle full ledger syntax (short dates, etc)
  ; @TODO: regexp simplifier!

  (let ((date-re (concat ; [0-9]{4}/[0-9]{2}/[0-9]{2}
		  "[0-9]\\{4\\}"
		  "/"
		  "[0-9]\\{2\\}"
		  "/"
		  "[0-9]\\{2\\}"
		  ))
	(status-re  "\\([*!]\\)?")
	(desc-re "\\([^:\n]+?\\)") ; anything but newline or ":"
	(memo-re "\\(: .*\\)?"))

  (looking-at (concat 
	       "\\(" date-re  "\\)"  ; initial date   (1)
	       "\\(=" date-re "\\)?" ; effective date (2)
	       "[ ]*"
	       status-re
	       "[ ]*"
	       desc-re
	       "[ ]*"
	       memo-re
	       "$" ; need this or the non-greedy match in desc-re
	           ; will only take the first character
	       ))))
	       

(defun goto-next-ledger-entry ()
  (interactive)
  (forward-line)
  (while (not (or (eobp)
		  (at-start-of-ledger-entry)))
    (forward-line))
  (print (ledger-parse-entry-at-point)))


;; @TODO: implement support for short (yearless) 
;; dates (I don't actually use them)

; returns either () or '(start date status entry-description)   
(defun ledger-parse-entry-at-point ()
  ; we wind up testing this twice because of the assertion,
  ; but without it this function could be called any time,
  ; and the global match vars might break
  (if (at-start-of-ledger-entry)
      (let ((posted    (match-string-no-properties 1))
	    (effective (match-string-no-properties 2))
	    (status    (match-string-no-properties 3))
	    (desc      (match-string-no-properties 4))
	    (memo      (match-string-no-properties 5)))
	(list posted effective status desc))
    nil))

; callback params: (posted effective status entry-description)
; where start is the position in the buffer and status is "*","!", or ""
(defun for-entry-in-ledger (callback)
  (catch 'stop
    (for-lines-from-point
     (lambda ()
       (when (at-start-of-ledger-entry)
	 (apply callback (ledger-parse-entry-at-point)))))))


(defmacro find-entry-where (&rest cond)
  `(progn
     (forward-line)
     (for-entry-in-ledger
      (lambda (posted effective status desc)
	(if ,@cond
	    (throw 'stop t))))
     (if (eobp) (message "no match found"))))


(defun find-entry-by-desc (goal-desc)
  (find-entry-where
     (and (not (equal status "*"))
	  (equal goal-desc desc))))

(defmacro current-entry-field (name)
  `(apply (lambda (posted effective status desc)
	    ,name)
	  (ledger-parse-entry-at-point)))

(defun current-entry-desc ()
  (current-entry-field desc))

(defmacro in-other-frame (&rest body)
  `(progn
     (other-frame 1)
     ,@body
     (other-frame 1)))

(defun find-next-ledger-match ()
  (interactive)
  (setq goal-desc (current-entry-desc))
  (in-other-frame
   (if (eobp) (beginning-of-buffer))
   (find-entry-by-desc goal-desc)))

(defun find-date-in-ledger (goal-date)
  (beginning-of-buffer)
  (find-entry-where
   (string< goal-date posted)))


(defun first-bank-entry ()
  (interactive)
  (beginning-of-buffer)
  (goto-next-ledger-entry)
  (in-other-frame
   (beginning-of-buffer))
  (find-next-ledger-match))


(defun cut-entry ()
  (interactive)
  (kill-paragraph 1))

(defun paste-entry ()
  (interactive)
  (yank)
  (backward-paragraph)
  (forward-line))

(defun copy-entry ()
  (interactive)
  (cut-entry)
  (paste-entry))


(defun accept-entry-match ()
  (interactive)
  (let ((goal-date (current-entry-field posted)))
       (cut-entry)
       (in-other-frame
	(if (not (equal goal-date (current-entry-field posted)))
	    (progn
	      (forward-char 10) ; 1234/67/9T
	      (insert "=")
	      (insert goal-date)))
	(ledger-toggle-current)
	(save-buffer))))
   



(defun copy-bank-entry-to-ledger ()
  (interactive)
  (let ((goal-date (current-entry-field posted)))
    (copy-entry)
    (in-other-frame
     (find-date-in-ledger goal-date)
     (yank)
     (insert "\n")
     (backward-paragraph 2)
     (goto-next-ledger-entry))))

(defun move-bank-entry-to-ledger ()
  (interactive)
  (copy-bank-entry-to-ledger)
  (cut-entry))

(defun move-and-accept-entry ()
  (interactive)
  (copy-bank-entry-to-ledger)
  (accept-entry-match))
