angular.module('starter.controllers', ['starter.services'])

.controller('AppCtrl', function($scope, $ionicModal, $timeout, $rootScope, $ionicHistory, $location, UserService, AuthenticationService) {

  // With the new view caching in Ionic, Controllers are only called
  // when they are recreated or on app start, instead of every page change.
  // To listen for when this page is active (for example, to refresh data),
  // listen for the $ionicView.enter event:
  //$scope.$on('$ionicView.enter', function(e) {
  //});

  $scope.$watch( AuthenticationService.IsLoggedIn, function ( IsLoggedIn ) {
    $scope.isLoggedIn = IsLoggedIn;
    $scope.currentUser = AuthenticationService.CurrentUser();
    if($scope.currentUser && $scope.currentUser.birth_date) {
      $scope.currentUser.birth_date = new Date($scope.currentUser.birth_date);// theDate.year(), theDate.month(), theDate.date()
    }
  });

  $scope.isUserLogged = function(){
    var user = $rootScope.globals.currentUser;
    console.log(user);
    if(user){
      return true;
    } else {
      return false;
    }
  }

  $scope.doLogOut = function() {
    AuthenticationService.ClearCredentials();
    $ionicHistory.nextViewOptions({disableBack: true});
    $location.path('app/login');
  }

  $scope.user = function() { 
    if($rootScope.globals.currentUser) {
      console.log("Return: " + JSON.stringify(user));
      return $rootScope.globals.currentUser.user;
    } else {
      return {};
    }
  }

  $scope.genderList = [
    {text: 'Male', value: 'male'},
    {text: 'Female', value: 'female'}
  ]

  /*
  $scope.getName = function () {
    if(plugins.appPreferences) {
      plugins.appPreferences.fetch(function(value){
        $scope.$apply(function(){$scope.name = value;});
        alert("I got this value: " + $scope.name);
      }, function(err){
        console.log(err);
      }, 'name');
    } else {
      return "Manuel";
    }
  };
  $scope.setName = function () {
    if(plugins.appPreferences) {
      plugins.appPreferences.store(function () {
        console.log('successfully saved!');
        alert("I saved: " + $scope.loginData.username);
        }, 
        function(){
          console.log('error setting reference...');
        }, 
        'name', 
        $scope.loginData.username
      );
    } else {
      console.log('nothing...');
    }
  };
  $scope.touchId = function(){
    $cordovaTouchID.checkSupport().then(function() {
      console.log('TouchID Available, using....');
      $cordovaTouchID.authenticate("Login plz").then(function() {
        alert('authenticated!');
      }, function () {
        alert('Something happened....');
      });
    }, function (error) {
      alert(error); // TouchID not supported
    });
  };
  */

})

.controller('PlaylistsCtrl', function($scope) {
  $scope.playlists = [
  { title: 'Reggae', id: 1 },
  { title: 'Chill', id: 2 },
  { title: 'Dubstep', id: 3 },
  { title: 'Indie', id: 4 },
  { title: 'Rap', id: 5 },
  { title: 'Cowbell', id: 6 }
  ];
})

.controller('LogInCtrl', function($scope, $ionicModal, $rootScope, $timeout, $location, $ionicHistory, $ionicPopup, UserService, AuthenticationService, FlashService) {
  $scope.loginData = {};
  $scope.registerData = {};

  // Perform the login action when the user submits the login form
  $scope.doLogin = function() {
    console.log('Doing login', $scope.loginData);
    $timeout(function() {
      AuthenticationService.Login($scope.loginData.email, $scope.loginData.password, function (response) {
        if (response.success) {
          AuthenticationService.SetCredentials($scope.loginData.email, $scope.loginData.password, response.user);
          $ionicHistory.nextViewOptions({disableBack: true});
          $location.path('app/home');
        } else {
          FlashService.Error(response.message);
          // An alert dialog
          $ionicPopup.alert({
            title: 'Login Failed.',
            template: 'The email or password may be incorrect.'
          });
        }
      });
    }, 1000);
  };


  // Perform the register action when the user submits the register form
  $scope.doRegister = function() {
    console.log('Doing register', $scope.registerData);
    $timeout(function() {
      $scope.registerData.username = $scope.registerData.email;
      $scope.registerData.birth_date = new Date($scope.registerData.birth_date);
      UserService.Create($scope.registerData);
      $scope.closeRegisterModal();
    }, 1000);
  };

  // Create the register modal that we will use later
  $ionicModal.fromTemplateUrl('templates/register.html', {
    scope: $scope
  }).then(function(modal) {
    $scope.modal = modal;
  });
  $scope.openRegisterModal = function() {
    $scope.modal.show();
  };
  $scope.closeRegisterModal = function() {
    $scope.modal.hide();
  };
  $scope.$on('$destroy', function() {
    $scope.modal.remove();
  });

})

.controller('ProfileCtrl', function($scope, $rootScope, UserService) {
  $scope.editing = false;

  // Perform the login action when the user submits the login form
  $scope.toggleEdit = function() {
    $scope.editing = !$scope.editing;
    if ($scope.editing) {
      console.log('Edit Profile ...');
    } else {
      console.log('Edit Profile Done ...');
    }
    
  };

  // Perform the login action when the user submits the login form
  $scope.saveProfile = function() {
    console.log('do nothing...');
  };

})

.controller('PlaylistCtrl', function($scope, $stateParams) {
});
