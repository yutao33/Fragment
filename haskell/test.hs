

data Node = Node Int Node Node
        | Empty
        deriving (Show)

root = Node 1 Empty (Node 2 Empty Empty)


len :: [a] -> Int
len [] = 0
len (x:xs) = 1 + (len xs)


-- average :: Num a =>[a] -> a
average [] = error "list length is 0"
average l = (sum l) / (fromIntegral (len l))
        where sum [] = 0
              sum (x:xs) = x + sum xs

-- func4 :: [a]->[a]
func4 l = l ++ (reverse2 l)
        where reverse2 [] = []
              reverse2 (x:xs) = (reverse2 xs) ++ (x:[])


help5 l a b = if a<b
              then ((l !! a) == (l !! b)) && help5 l (a+1) (b-1)
              else True
-- func5 :: [a] -> Bool
func5 l = help5 l 0 ((len l)-1)