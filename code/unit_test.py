import mapgenerator
import unittest, json

class TestMapGenerator(unittest.TestCase):
     
    def test_common_nb(self):
        MG_test = mapgenerator.MapGenerator()
        self.assertEqual(MG_test.common_nb(["grass7", "water11", "grass0", "path8"], ["path4", "water0",  "grass0", "path8"]), ["grass0", "path8"])


    def test_is_fully_collapsed(self):
        MG_not_collapsed = mapgenerator.MapGenerator()
        MG_collapsed = mapgenerator.MapGenerator()      
        MG_not_collapsed.grid = [[[1,1,1,1], [1,1,1,1]], [[1,1,1,1], [1,1,1,1]], [[1,1,1,1], [1,1,1,1]]]
        MG_collapsed.grid = [[[1,], [1]], [[1], [1]], [[1], [1]]]
        self.assertEqual(MG_not_collapsed.is_fully_collapsed(), False)
        self.assertEqual(MG_collapsed.is_fully_collapsed(), True)


    def test_get_valid_nbs(self):
        MG_test = mapgenerator.MapGenerator()
        file = open('Data/nb_rules.json')
        data = json.load(file)
        data = data["data"]    
        up =  ["grass0", "grass1", "grass2", "grass3", "flower", "tall_grass", "tree_cut", "path4", "path5", "path6", "water6", "water7", "water8"]
        down = ["grass0", "grass1", "grass2", "grass3", "flower", "tall_grass", "tree_cut", "path3", "path7", "path8", "water0", "water1", "water2"]
        left = ["grass0", "grass1", "grass2", "grass3", "flower", "tall_grass", "tree_cut", "path2", "path6", "path8", "water2", "water5", "water8"]
        right = ["grass0", "grass1", "grass2", "grass3", "flower", "tall_grass", "tree_cut", "path1", "path5", "path7", "water0", "water3", "water6"]
        diag_lu = ["grass0", "grass1", "grass2", "grass3", "flower", "tall_grass", "tree_cut", "path2", "path4", "path5", "path6", "path8", "water2", "water5", "water6", "water7", "water8", "water11"]
        diag_ru = ["grass0", "grass1", "grass2", "grass3", "flower", "tall_grass", "tree_cut", "path1", "path4", "path5", "path6", "path7", "water0", "water3", "water6", "water7", "water8", "Water12"]
        diag_ld = ["grass0", "grass1", "grass2", "grass3", "flower", "tall_grass", "tree_cut", "path2", "path3", "path6", "path7", "path8", "water0", "water1", "water2", "water5", "water8", "Water10"]
        diag_rd = ["grass0", "grass1", "grass2", "grass3", "flower", "tall_grass", "tree_cut", "path1", "path3", "path5", "path7", "path8", "water0", "water1", "water2","water3", "water6", "water9"]
        self.assertEqual(MG_test.get_valid_nbs("flower", data), [up, down, left, right, diag_lu, diag_ru, diag_ld, diag_rd])
        file.close()


if __name__ == "__main__":
    unittest.main()