(defn HumanizeTime [^int seconds]
    (setv count 0
        ping_time ""
        time_list []
        time_suffix_list ["s" "m" "h" "days"])
    (while (< count 4)
        (+= count 1)
        (if (< count 3)
            (setv (, remainder result) (divmod seconds 60))
            (setv (, remainder result) (divmod seconds 24)))
        (if (and (= seconds 0) (= remainder 0))
            (break))
        (time_list.append (int result))
        (setv seconds (int remainder)))
    (for [x (range (len time_list))]
        (assoc time_list x (+ (str (get time_list x)) (get time_suffix_list x))))
    (if (= (len time_list) 4)
        (+= ping_time f"{(time_list.pop)}"))
    (time_list.reverse)
    (+= ping_time (.join ":" time_list))
    (return ping_time))
