# coding: utf-8

from __future__ import absolute_import

from flask import json
from swagger_server.models.air_quality_value import AirQualityValue  # noqa: E501
from swagger_server.models.co2_value import CO2Value  # noqa: E501
from swagger_server.models.humidity_value import HumidityValue  # noqa: E501
from swagger_server.models.light_intensity_value import LightIntensityValue  # noqa: E501
from swagger_server.models.room_facilities import RoomFacilities  # noqa: E501
from swagger_server.models.sound_value import SoundValue  # noqa: E501
from swagger_server.models.temperature_value import TemperatureValue  # noqa: E501
from swagger_server.models.voc_value import VOCValue  # noqa: E501
from swagger_server.test import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    def test_air_quality_room_name_get(self):
        """Test case for air_quality_room_name_get

        Retrieve air quality of a room
        """
        response = self.client.open(
            "/Air_Quality/{room_name}".format(room_name="room_name_example"),
            method="GET",
        )
        self.assert200(response, "Response body is : " + response.data.decode("utf-8"))

    def test_air_quality_room_name_post(self):
        """Test case for air_quality_room_name_post

        Add a new air quality value to a room
        """
        body = AirQualityValue()
        response = self.client.open(
            "/Air_Quality/{room_name}".format(room_name="room_name_example"),
            method="POST",
            data=json.dumps(body),
            content_type="application/json",
        )
        self.assert200(response, "Response body is : " + response.data.decode("utf-8"))

    def test_c_o2_room_name_get(self):
        """Test case for c_o2_room_name_get

        Retrieve CO2 levels of a room
        """
        response = self.client.open(
            "/CO2/{room_name}".format(room_name="room_name_example"), method="GET"
        )
        self.assert200(response, "Response body is : " + response.data.decode("utf-8"))

    def test_c_o2_room_name_post(self):
        """Test case for c_o2_room_name_post

        Add a new CO2 level value to a room
        """
        body = CO2Value()
        response = self.client.open(
            "/CO2/{room_name}".format(room_name="room_name_example"),
            method="POST",
            data=json.dumps(body),
            content_type="application/json",
        )
        self.assert200(response, "Response body is : " + response.data.decode("utf-8"))

    def test_humidity_room_name_get(self):
        """Test case for humidity_room_name_get

        Retrieve humidity levels of a room
        """
        response = self.client.open(
            "/Humidity/{room_name}".format(room_name="room_name_example"), method="GET"
        )
        self.assert200(response, "Response body is : " + response.data.decode("utf-8"))

    def test_humidity_room_name_post(self):
        """Test case for humidity_room_name_post

        Add a new humidity level value to a room
        """
        body = HumidityValue()
        response = self.client.open(
            "/Humidity/{room_name}".format(room_name="room_name_example"),
            method="POST",
            data=json.dumps(body),
            content_type="application/json",
        )
        self.assert200(response, "Response body is : " + response.data.decode("utf-8"))

    def test_light_intensity_room_name_get(self):
        """Test case for light_intensity_room_name_get

        Retrieve light intensity levels of a room
        """
        response = self.client.open(
            "/Light_Intensity/{room_name}".format(room_name="room_name_example"),
            method="GET",
        )
        self.assert200(response, "Response body is : " + response.data.decode("utf-8"))

    def test_light_intensity_room_name_post(self):
        """Test case for light_intensity_room_name_post

        Add a new light intensity value to a room
        """
        body = LightIntensityValue()
        response = self.client.open(
            "/Light_Intensity/{room_name}".format(room_name="room_name_example"),
            method="POST",
            data=json.dumps(body),
            content_type="application/json",
        )
        self.assert200(response, "Response body is : " + response.data.decode("utf-8"))

    def test_room_facilities_room_name_get(self):
        """Test case for room_facilities_room_name_get

        Retrieve room facilities of a room
        """
        response = self.client.open(
            "/Room_Facilities/{room_name}".format(room_name="room_name_example"),
            method="GET",
        )
        self.assert200(response, "Response body is : " + response.data.decode("utf-8"))

    def test_room_facilities_room_name_post(self):
        """Test case for room_facilities_room_name_post

        Add or update room facilities for a room
        """
        body = RoomFacilities()
        response = self.client.open(
            "/Room_Facilities/{room_name}".format(room_name="room_name_example"),
            method="POST",
            data=json.dumps(body),
            content_type="application/json",
        )
        self.assert200(response, "Response body is : " + response.data.decode("utf-8"))

    def test_room_facilities_room_name_put(self):
        """Test case for room_facilities_room_name_put

        Update room facilities
        """
        body = RoomFacilities()
        response = self.client.open(
            "/Room_Facilities/{room_name}".format(room_name="room_name_example"),
            method="PUT",
            data=json.dumps(body),
            content_type="application/json",
        )
        self.assert200(response, "Response body is : " + response.data.decode("utf-8"))

    def test_room_list_get(self):
        """Test case for room_list_get

        Retrive a list of room
        """
        response = self.client.open("/RoomList", method="GET")
        self.assert200(response, "Response body is : " + response.data.decode("utf-8"))

    def test_room_list_post(self):
        """Test case for room_list_post

        Add a new AirQualityRoom
        """
        body = "body_example"
        response = self.client.open(
            "/RoomList",
            method="POST",
            data=json.dumps(body),
            content_type="application/json",
        )
        self.assert200(response, "Response body is : " + response.data.decode("utf-8"))

    def test_rooms_room_name_delete(self):
        """Test case for rooms_room_name_delete

        Delete a Room
        """
        response = self.client.open(
            "/Rooms/{room_name}".format(room_name="room_name_example"), method="DELETE"
        )
        self.assert200(response, "Response body is : " + response.data.decode("utf-8"))

    def test_rooms_room_name_get(self):
        """Test case for rooms_room_name_get

        Retrive a list of room
        """
        response = self.client.open(
            "/Rooms/{room_name}".format(room_name="room_name_example"), method="GET"
        )
        self.assert200(response, "Response body is : " + response.data.decode("utf-8"))

    def test_rooms_room_name_put(self):
        """Test case for rooms_room_name_put

        Update room name
        """
        body = "body_example"
        response = self.client.open(
            "/Rooms/{room_name}".format(room_name="room_name_example"),
            method="PUT",
            data=json.dumps(body),
            content_type="application/json",
        )
        self.assert200(response, "Response body is : " + response.data.decode("utf-8"))

    def test_sound_room_name_get(self):
        """Test case for sound_room_name_get

        Retrieve sound levels of a room
        """
        response = self.client.open(
            "/Sound/{room_name}".format(room_name="room_name_example"), method="GET"
        )
        self.assert200(response, "Response body is : " + response.data.decode("utf-8"))

    def test_sound_room_name_post(self):
        """Test case for sound_room_name_post

        Add a new sound level value to a room
        """
        body = SoundValue()
        response = self.client.open(
            "/Sound/{room_name}".format(room_name="room_name_example"),
            method="POST",
            data=json.dumps(body),
            content_type="application/json",
        )
        self.assert200(response, "Response body is : " + response.data.decode("utf-8"))

    def test_temperature_room_name_get(self):
        """Test case for temperature_room_name_get

        Retrieve temperature of a room
        """
        response = self.client.open(
            "/Temperature/{room_name}".format(room_name="room_name_example"),
            method="GET",
        )
        self.assert200(response, "Response body is : " + response.data.decode("utf-8"))

    def test_temperature_room_name_post(self):
        """Test case for temperature_room_name_post

        Add a new temperature value to a room
        """
        body = TemperatureValue()
        response = self.client.open(
            "/Temperature/{room_name}".format(room_name="room_name_example"),
            method="POST",
            data=json.dumps(body),
            content_type="application/json",
        )
        self.assert200(response, "Response body is : " + response.data.decode("utf-8"))

    def test_v_oc_room_name_get(self):
        """Test case for v_oc_room_name_get

        Retrieve VOC levels of a room
        """
        response = self.client.open(
            "/VOC/{room_name}".format(room_name="room_name_example"), method="GET"
        )
        self.assert200(response, "Response body is : " + response.data.decode("utf-8"))

    def test_v_oc_room_name_post(self):
        """Test case for v_oc_room_name_post

        Add a new VOC value to a room
        """
        body = VOCValue()
        response = self.client.open(
            "/VOC/{room_name}".format(room_name="room_name_example"),
            method="POST",
            data=json.dumps(body),
            content_type="application/json",
        )
        self.assert200(response, "Response body is : " + response.data.decode("utf-8"))


if __name__ == "__main__":
    import unittest

    unittest.main()
