angular.module('webApp', [])
  .controller('webController', ['$scope', '$filter', '$http', '$compile', function($scope, $filter, $http, $compile) {
    
    $scope.init = function() {
        console.log("Begin Init");
        
        $scope.showApps = true;
    }
    
    $scope.submit = function() {
        console.log("Submitted");
    }
    
  }]);