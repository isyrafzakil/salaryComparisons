angular.module('webApp', [])
  .controller('webController', ['$scope', '$filter', '$http', '$compile', function($scope, $filter, $http, $compile) {
    
    $scope.init = function() {
        console.log("Begin Init");
        
        $scope.showApps = true;
    }
    
    $scope.submit = function(jobTitle, yrsOfExp) {
        console.log("Job Title: ", jobTitle, "\nYears of Exp: ", yrsOfExp, " years");
        $scope.jobTitle = jobTitle;
        $scope.yrsOfExp = yrsOfExp;
    }
    
  }]);