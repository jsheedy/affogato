'use strict';

angular.module('affogatoApp')
.controller('MainCtrl', function ($scope, affogatoAPI, leafletData) {
  $scope.center = {
    lat: 47.6,
    lng: -122.2,
    zoom: 12
  };

  $scope.counter = undefined;

  var counterClick = function(feature) {
    $scope.counter = feature.properties;
  }

  var addCounters = function() {
    leafletData.getMap('mainmap').then(function(map) {
      var layer = L.geoJson($scope.counters, {
        pointToLayer: function (feature, latlng) {
          return L.circleMarker(latlng, {
            fillColor: '#f00',
            color: '#000',
            fillOpacity: 1.0,
            opacity: 1.0,
            weight: 1,
            radius: 10,
            stroke: true
          });
        },
        onEachFeature: function(f, layer) {
          layer.on({
            click: function(e) {
              counterClick(f, e.latng);
            },
            // mouseover: function(e) {geojsonMouseover(e, feature);},
            // mouseout: function(e) {geojsonMouseout(e, feature); }
          });
        }
      }).addTo(map);
    });
  };
  $scope.counters = affogatoAPI.Counters.get({}, addCounters);

});
