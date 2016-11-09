head' :: [a] -> a
head' [] = undefined
head' (a:_) = a

tail' :: [a] -> [a]
tail' [] = []
tail' (a:b) = b

take' :: Int -> [a] -> [a]
take' 0 a = []
take' n [] = []
take' n (a:b) = a:(take' (n-1) b)

drop' :: Int -> [a] -> [a]
drop' 0 a = a
drop' n [] = []
drop' n (a:b) = drop' (n-1) b

filter' :: (a -> Bool) -> [a] -> [a]
filter' f [] = []
filter' f (a:b) | f a = a : (filter' f b)
                | True = (filter' f b)

foldl' :: (a -> b -> a) -> a -> [b] -> a
foldl' f z [] = z
foldl' f z (a:b) = foldl' f (f z a) b

concat' :: [a] -> [a] -> [a]
concat' [] b = b
concat' (a:a') b = a : (concat' a' b)

quickSort' :: Ord a => [a] -> [a]
quickSort' [] = []
quickSort' a = concat' (concat' (quickSort' (filter' less' a)) (filter' equal' a)) (quickSort' (filter' greater' a))
               where h' = head' a
                     less' = (< h')
                     equal' = (h' ==)
                     greater' = (> h')

