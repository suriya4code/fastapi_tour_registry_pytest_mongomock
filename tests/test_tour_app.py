import pytest
from unittest.mock import patch


from src.api.tour_app import Tour, TourList, index, add_tour, get_tour_by_place, add_tour_list
from src.api.tour_app import update_tour_by_place, delete_tour_by_place


class TestTour():

    @pytest.fixture(autouse=True)
    def _get_mongo(self, mongodb):
        self.db = mongodb

    def test_index(self):
        with patch('src.api.tour_app.get_Collection') as mock_mongo:
            mock_mongo.return_value = self.db.tour_registry
            resp = index()
            assert len(resp["data"]) > 0
    
    def test_add_tour(self):
        with patch('src.api.tour_app.get_Collection') as mock_mongo:
            mock_mongo.return_value = self.db.tour_registry
            data = Tour(tour_id=101,place="Chennnai", country="India", is_visa_needed=False, budget=10000)
            resp = add_tour(data=data)
            assert resp["status"] == "success"
    
    def test_add_tour_list(self):
        with patch('src.api.tour_app.get_Collection') as mock_mongo:
            mock_mongo.return_value = self.db.tour_registry
            data1 = Tour(tour_id=101,place="Chennnai", country="India", is_visa_needed=False, budget=10000)
            data2 = Tour(tour_id=101,place="Erode", country="India", is_visa_needed=False, budget=10000)
            tour_list_data = TourList(data=[data1,data2])
            resp = add_tour_list(request=tour_list_data)
            assert resp["status"] == "success"

    def test_get_tour_by_place(self):
        with patch('src.api.tour_app.get_Collection') as mock_mongo:
            mock_mongo.return_value = self.db.tour_registry
            resp = get_tour_by_place("NewYork1")
            assert len(resp["data"]) > 0
    
    def test_update_tour_by_place(self):
        with patch('src.api.tour_app.get_Collection') as mock_mongo:
            mock_mongo.return_value = self.db.tour_registry
            data = Tour(tour_id=101,place="Chennnai", country="India", is_visa_needed=False, budget=10000)
            resp = update_tour_by_place(place="NewYork1",data=data)
            assert resp["status"] == "success"
    
    def test_delete_tour_by_place(self):
        with patch('src.api.tour_app.get_Collection') as mock_mongo:
            mock_mongo.return_value = self.db.tour_registry
            resp = delete_tour_by_place("NewYork1")
            assert resp["status"] == "success"