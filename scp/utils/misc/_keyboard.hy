(import [scp[user]])


(defclass _KB [user.types.InlineKeyboardButton]
    (defn __eq__ [self other]
        (return (= self.text other.text)))
    
    (defn __lt__ [self other]
        (return (< self.text other.text)))
    
    (defn __gt__ [self other]
        (return (> self.text other.text))))
