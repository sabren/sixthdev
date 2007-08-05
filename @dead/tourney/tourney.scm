
;$Id$

;; couldn't get schemeunit working:
(define (assert condition)
  (if (not (eval condition))
      (begin 
	(display "failed: ")
	(display condition)
	(newline))))

(define (asserteq msg a b)
  (if (not (eq? a b))
      (begin 
	(display msg)
	(display "failed: ")
	(display a)
	(display " != ")
	(display b)
	(newline))))

(define (winner game players) 
  (eval (cons game players)))


;; roshambo ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(define rock 'rock)
(define paper 'paper)
(define scissors 'scissors)

(define advantage 
  ;; first beats second:
  (list (list paper rock)
	(list rock scissors)
	(list scissors paper)))

(define (match a b advantages)
  (cond ((null? advantages) "error: couldn't determine winner!")
        ((equal? (list a b) (car advantages)) a)
	((equal? (list b a) (car advantages)) b)
	(else (match a b (cdr advantages)))))

(define (roshambo a b)
  (if (eq? a b) 
      a
      (match a b advantage)))
        

;; TEST CASES ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(define (tests)
  ;; tournament:
  (assert '(= 5 (winner max '(1 2 3 4 5))))
  (assert '(= 4 (winner max '(4 3 2 1 0))))
  (assert '(= 5 (winner max '(1 3 5 2 4))))
  (assert '(= 1 (winner min '(1 3 5 2 4))))

  ;; roshambo:
  (asserteq 1 rock (roshambo rock scissors))
  (asserteq 2 rock (roshambo scissors rock))
  (asserteq 3 paper (roshambo paper rock))
  (asserteq 4 paper (roshambo rock paper))
  (asserteq 5 scissors (roshambo scissors paper))
  (asserteq 6 scissors (roshambo paper scissors))

  (asserteq 7 rock (roshambo rock rock))
  (asserteq 8 paper (roshambo paper paper))
  (asserteq 9 scissors (roshambo scissors scissors))
  )

(tests)
