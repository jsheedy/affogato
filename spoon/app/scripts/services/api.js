'use strict';

angular.module('affogatoApp')
  .factory('affogatoAPI', function ($resource, CONFIG) {

    var resourceFactory = function(apiPath) {
      return $resource(CONFIG.apiURL + apiPath, {}, {get: {method: 'GET', cache: true}});
    };

    var methods = {

      Counters: resourceFactory('counters/'),
      Counter: resourceFactory('counters/:id'),
      CounterData: resourceFactory('counters/:id/data/'),
      CounterDataDeseasonalized: resourceFactory('counters/:id/data/deseasonalized/'),
      apiURL: CONFIG.apiURL
    };

    return methods;
  });