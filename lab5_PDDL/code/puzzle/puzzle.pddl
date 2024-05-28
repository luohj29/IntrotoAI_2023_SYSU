(define (domain puzzle)
  (:requirements :strips :typing:equality
                 :universal-preconditions
                 :conditional-effects)
  (:types num loc) 
  (:predicates  (at ?tile - num ?pos - loc) 
        (blank ?pos - loc)
        (neighbor ?pos_1 - loc ?pos_2 - loc)
  )

  

  (:action slide
             :parameters (?tile - num ?pos_1 - loc ?pos_2 - loc)
             :precondition (and (at ?tile  ?pos_1) (blank ?pos_2) (neighbor ?pos_1 ?pos_2))
             :effect (and (at ?tile  ?pos_2) (blank ?pos_1) (not (blank ?pos_2)) (not (at ?tile  ?pos_1))) 
  )
)