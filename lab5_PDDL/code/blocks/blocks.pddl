(define (domain blocks)
  (:requirements :strips :typing:equality
                 :universal-preconditions
                 :conditional-effects)
  (:types physob)
  (:predicates   
        (ontable ?x - physob)
        (clear ?x - physob) 
        (on ?x ?y - physob))
  
  (:action move
            :parameters (?x ?y - physob)  
            :precondition (and (clear ?x)
                        (clear ?y)
                        (not(= ?x ?y))
                        )
             :effect (and (on ?x ?y)
                        (not (clear ?y))
                        (forall (?z - physob)
                        (when (on ?x ?z)(and (not(on ?x ?z))(clear ?z))))))

  (:action moveToTable
                    :parameters (?x - physob)
                    :precondition (clear ?x)
                    :effect (and (ontable ?x)
                        (forall (?z - physob)
                        (when (on ?x ?z)(and (not(on ?x ?z))(clear ?z))))))
)
              
