
;; couldn't get schemeunit working:
(define (assert condition)
  (if (not (eval condition))
      (begin 
	(display "failed: ")
	(display condition)
	(newline))))

(define (winner game players) 
  (eval (cons game players)))

(define (tournament-tests)
  (assert '(= 5 (winner max '(1 2 3 4 5))))
  (assert '(= 4 (winner max '(4 3 2 1 0))))
  (assert '(= 55 (winner max '(1 3 5 2 4))))
  (assert '(= 1 (winner min '(1 3 5 2 4)))))

(tournament-tests)
