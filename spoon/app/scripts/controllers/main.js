'use strict';

angular.module('affogatoApp')
.controller('MainCtrl', function ($scope) {
 $scope.center = {
  lat: 47.6,
  lng: -122.3,
  zoom: 11
};
});