import Prelude hiding (lookup)

data BinaryTree k v = Null | Node {  left  :: BinaryTree k v
                                  ,  right :: BinaryTree k v
                                  ,  key   :: k
                                  ,  val   :: v
                                  }

lookup :: Ord k => k -> BinaryTree k v -> Maybe v
lookup k' Null = Nothing
lookup k' t | key t == k' = Just (val t)
            | key t > k' = lookup k' (left t)
            | True = lookup k' (right t)


insert :: Ord k => k -> v -> BinaryTree k v -> BinaryTree k v
insert k v Null = Node Null Null k v
insert k v t | key t == k = Node (left t) (right t) k v
             | key t > k = Node (insert k v (left t)) (right t) (key t) (val t)
             | True = Node (left t) (insert k v (right t)) (key t) (val t)

--assuming k1 < k2
merge' :: Ord k => BinaryTree k v -> BinaryTree k v -> BinaryTree k v
merge' t1 Null = t1
merge' Null t2 = t2
merge' t1 t2 = Node (left t1) (merge' (right t1) t2) (key t1) (val t1)


delete :: Ord k => k -> BinaryTree k v -> BinaryTree k v
delete k Null = Null
delete k t | key t == k = merge' (left t) (right t)
           | key t > k = Node (delete k (left t)) (right t) (key t) (val t)
           | True = Node (left t) (delete k (right t)) (key t) (val t)
