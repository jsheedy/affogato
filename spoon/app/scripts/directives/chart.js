'use strict';
angular.module('affogatoApp')
  .directive('affogatoChart', function(affogatoAPI, $window) {
    var controller = function($scope, $element) {
      var container = d3.select($element[0]);

      $scope.updateData = function() {

        var width = container.node().getBoundingClientRect().width;
        var height = container.node().getBoundingClientRect().height;
        var timeParser = d3.time.format('%Y-%m-%d');
        var x = d3.time.scale()
          .domain([
            timeParser.parse('2012-10-01'),
            new Date()])
          .range([0,width]);

        var svg = container.select('svg');
        svg
          .attr('width', width)
          .attr('height', height);

        var max = d3.max($scope.data.data, function(x) {return x[$scope.field];})
        var y = d3.scale.linear()
          .domain([0,max])
          .range([height,0]);

        svg.selectAll('*').remove();

        var yAxis = d3.svg.axis()
          .scale(y)
          .orient("left")
          .ticks(5);

        svg.append("g")
            .attr("class", "axis")
            .attr("transform", "translate(" + 0 + ",0)")
            .call(yAxis);

        var line = d3.svg.line()
                .x(function(d) { return x(timeParser.parse(d.datetime)); })
                .y(function(d) { return y(d[$scope.field]); });


        svg.append("path").datum($scope.data.data)
          .transition()
          .attr("class", "line")
          .attr("d", line);


        // var barWidth = width / $scope.data.data.length;
        // var bars = svg.selectAll('rect')
        //   .data($scope.data.data, function(d) {return d['datetime'];})
        // bars.enter()
        //   .append('rect')
        //   .attr('x', function(d, i) { return x(d3.time.format('%Y-%m-%d').parse(d['datetime'])); })
        //   .attr('width', barWidth);

        // bars.transition()
        //   .attr('y', function(d) { return y(d[$scope.field]) ; })
        //   .attr("height", function(d) { return height - y(d[$scope.field]); });

        // bars.exit().remove();
      };

      window.onresize = function() {
        $scope.$apply();
      };

      $scope.$watch('counter', function() {
        if (!($scope.counter && $scope.counter.id)) {
          return;
        }
        if ($scope.type === 'raw') {
          $scope.data = affogatoAPI.CounterData.get({id: $scope.counter.id, aggregate: 'daily'}, $scope.updateData);
        } else if ($scope.type === 'deseasonalized') {
          $scope.data = affogatoAPI.CounterDataDeseasonalized.get({id: $scope.counter.id}, $scope.updateData);
        }
      });

      $scope.$watch(function() {
        return angular.element($window)[0].innerWidth;
      }, function() {
        $scope.updateData();
      });


  };
  return {
    replace: true,
    restrict: 'E',
    scope: {
      counter: '=',
      type: '@',
      field: '@'
    },
    templateUrl: 'views/affogato-chart.html',
    controller: controller
  };
});
