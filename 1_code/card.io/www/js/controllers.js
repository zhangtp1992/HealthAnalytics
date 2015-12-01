var staticMap = "https://maps.googleapis.com/maps/api/staticmap?key=AIzaSyBCxCvlC1kBSNGd0WEvsN5X0BkqDQTdIdo";
angular.module('starter.controllers', ['starter.services'])

.controller('AppCtrl', function($scope, $ionicModal, $timeout, $rootScope, $ionicHistory, $location, md5, UserService, AuthenticationService) {

  // With the new view caching in Ionic, Controllers are only called
  // when they are recreated or on app start, instead of every page change.
  // To listen for when this page is active (for example, to refresh data),
  // listen for the $ionicView.enter event:
  //$scope.$on('$ionicView.enter', function(e) {
  //});
  // Gravatar size
  
  // Variables and static data needed 
  $scope.gSize = 200;

  $scope.genderList = [
    {text: 'Male', value: 'm'},
    {text: 'Female', value: 'f'}
  ]

  $scope.stateList = [
    { value: 'AL', text: 'Alabama' }, { value: 'AK', text: 'Alaska' },
    { value: 'AZ', text: 'Arizona' }, { value: 'AR', text: 'Arkansas' },
    { value: 'CA', text: 'California' }, { value: 'CO', text: 'Colorado' },
    { value: 'CT', text: 'Connecticut' }, { value: 'DE', text: 'Delaware' },
    { value: 'FL', text: 'Florida' }, { value: 'GA', text: 'Georgia' },
    { value: 'HI', text: 'Hawaii' }, { value: 'ID', text: 'Idaho' },
    { value: 'IL', text: 'Illinois' }, { value: 'IN', text: 'Indiana' },
    { value: 'IA', text: 'Iowa' }, { value: 'KS', text: 'Kansas' },
    { value: 'KY', text: 'Kentucky' }, { value: 'LA', text: 'Louisiana' },
    { value: 'ME', text: 'Maine' }, { value: 'MD', text: 'Maryland' },
    { value: 'MA', text: 'Massachusetts' }, { value: 'MI', text: 'Michigan' },
    { value: 'MN', text: 'Minnesota' }, { value: 'MS', text: 'Mississippi' },
    { value: 'MO', text: 'Missouri' }, { value: 'MT', text: 'Montana' },
    { value: 'NE', text: 'Nebraska' }, { value: 'NV', text: 'Nevada' },
    { value: 'NH', text: 'New Hampshire' }, { value: 'NJ', text: 'New Jersey' },
    { value: 'NM', text: 'New Mexico' }, { value: 'NY', text: 'New York' },
    { value: 'NC', text: 'North Carolina' }, { value: 'ND', text: 'North Dakota' },
    { value: 'OH', text: 'Ohio' }, { value: 'OK', text: 'Oklahoma' },
    { value: 'OR', text: 'Oregon' }, { value: 'PA', text: 'Pennsylvania' },
    { value: 'RI', text: 'Rhode Island' }, { value: 'SC', text: 'South Carolina' },
    { value: 'SD', text: 'South Dakota' }, { value: 'TN', text: 'Tennessee' },
    { value: 'TX', text: 'Texas' }, { value: 'UT', text: 'Utah' },
    { value: 'VT', text: 'Vermont' }, { value: 'VA', text: 'Virginia' },
    { value: 'WA', text: 'Washington' }, { value: 'WV', text: 'West Virginia' },
    { value: 'WI', text: 'Wisconsin' }, { value: 'WY', text: 'Wyoming' }
  ]


  // Watch for the set current user and update the birthdate.
  $scope.$watch( $scope.isUserLogged , function ( isUserLogged ) {
    $scope.currentUser = AuthenticationService.CurrentUser().user;
    if($scope.currentUser && $scope.currentUser.birth_date) {
      $scope.currentUser.birth_date = new Date($scope.currentUser.birth_date);// theDate.year(), theDate.month(), theDate.date()
    }
  });

  $scope.isUserLogged = function(){
    return AuthenticationService.IsLoggedIn();
  }

  $scope.doLogOut = function() {
    AuthenticationService.Logout();
    $ionicHistory.nextViewOptions({disableBack: true});
    $location.path('app/login');
  }
  
  $scope.gravatarUrl = function() {
    return 'http://www.gravatar.com/avatar/' + md5.createHash($scope.currentUser.email.toLowerCase()) + '?s=' + $scope.gSize;
  }

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

  $scope.$watch( $scope.registerData.birth_date, function ( birth_date ) {
    $scope.registerData.birth_date = new Date(birth_date);
  });

  // Perform the login action when the user submits the login form
  $scope.doLogin = function() {
    console.log('Doing login', $scope.loginData);
    AuthenticationService.Login($scope.loginData.email, $scope.loginData.password, 
    function (response) {
      if (response.success) {
        $ionicHistory.nextViewOptions({disableBack: true});
        $location.path('app/home');
      } else {
        FlashService.Error(response.data);
        // An alert dialog
        $ionicPopup.alert({
          title: 'Login Failed.',
          template: response.data
        });
      }
    });
  };


  // Perform the register action when the user submits the register form
  $scope.doRegister = function() {
    console.log('Doing register', $scope.registerData);
    $scope.registerData.username = $scope.registerData.email;
    $scope.registerData.birth_date = new Date($scope.registerData.birth_date);
    UserService.Create($scope.registerData).then(function (response){
      if(response.success) {
        $scope.closeRegisterModal();
      } else {
        // An alert dialog
        $ionicPopup.alert({
          title: 'Registration Failed.',
          template: response.data
        });
      }
    });
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
  $scope.$on('modal.hidden', function() {
    $scope.registerData = {};
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

.controller('SettingsCtrl', function($scope, $stateParams) {
})

.controller('AddWorkoutCtrl', function($scope, $stateParams) {
  $scope.workoutTypes = [
    {text: 'Run', value: 'run'},
    {text: 'Walk', value: 'Walk'},
    {text: 'Bike', value: 'bike'},
  ];
  var now = moment();
  var name = 'Run on ' + (now.month()+1) + '/' + now.date() + '/' + now.year();
  $scope.workoutData = {name: name, type: 'run', date: new Date(now.year(), now.month(), now.date()), distance: 0.0, duration: 0.0};
})

.controller('AddFoodCtrl', function($scope, $stateParams) {
  var now = moment();
  $scope.foodData = {type: 'lunch', food: "coffee", serving: '0.5', date: new Date(now.year(), now.month(), now.date())};

  $scope.foodTypes = [
    {text: 'Pizza', value: 'pizza', calories: 215},
    {text: 'Coffee', value: 'coffee', calories: 130},
    {text: 'Cake', value: 'cake', calories: 600}
  ];

  $scope.mealTypes = [
    {text: 'Breakfast', value: 'breakfast'},
    {text: 'Lunch', value: 'lunch'},
    {text: 'Dinner', value: 'dinner'},
    {text: 'Snack', value: 'snack'},
    {text: 'Other', value: 'other'}
  ];

  $scope.servingTypes = [
    {text: 'A Lot', value: '3'},
    {text: 'Moderate', value: '2'},
    {text: 'Normal', value: '1'},
    {text: 'Quick Snack', value: '0.5'}
  ];
})

.controller('WorkoutsCtrl', function($scope, $stateParams, AuthenticationService, WorkoutService) {
  $scope.username = AuthenticationService.CurrentUser().username;
  
  WorkoutService.GetAll($scope.username).then(function (response){
    if (response.success) {
      $scope.workoutList = response.data;
    }
  });
  

  $scope.formatDate = function(date) {
    if(date) {
      console.log(date);
      console.log(moment(date).format('LL'));
      return moment(date).format('LL');
    }
  }

  $scope.formatDuration = function(minutes){
    if(minutes){
      var hours = parseInt( minutes / 60 );
      var minutes = parseInt( minutes % 60 );
      var seconds = parseInt( (minutes % 60.0) / 60 );
      var result = (hours < 10 ? "0" + hours : hours) + ":" + (minutes < 10 ? "0" + minutes : minutes) + ":" + (seconds  < 10 ? "0" + seconds : seconds);
      return result;
    }
  }

  $scope.formatPace = function(pace){
    if(pace && pace > 0) {
      var minutes = parseInt( pace / 60 );
      var seconds = parseInt(pace % 60);
      var result = (minutes < 10 ? "0" + minutes : minutes) + ":" + (seconds  < 10 ? "0" + seconds : seconds) + " min/mi.";
      return result;
    }
  }

  $scope.getWorkoutIcon = function(foodName) {
    var foods = {
      'walk': 'ion-android-walk',
      'jog': 'ion-ribbon-a',
      'bike': 'ion-android-bicycle'
    };
    var retIcon = foods[foodName.toLowerCase()];
    return retIcon || 'ion-ribbon-a';
  }

  /*

  [
  {"workout_id":50,"workout_type":"jog","distance":2,"duration":65,"calories":250,"pace":1,"workout_timestamp":"2015-11-05T13:12:43.511Z","email":"ntaylor@aps.rutgers.edu"},
  {"workout_id":51,"workout_type":"jog","distance":2,"duration":65,"calories":250,"pace":1,"workout_timestamp":"2015-11-05T13:12:43.511Z","email":"ntaylor@aps.rutgers.edu"},
  {"workout_id":52,"workout_type":"jog","distance":2,"duration":65,"calories":250,"pace":1,"workout_timestamp":"2015-11-05T13:12:43.511Z","email":"ntaylor@aps.rutgers.edu"}
  ]
  
  [
    {id: '1', name: "Nice walk in Johnson Park", type: 'walk', icon:'ion-android-walk', date: new Date("2015", "10", "02"), distance: 1.1, duration: 1260.0, gmap: staticMap + '&path=40.511827,-74.462018|40.514736,-74.478021&center=Highpoint+Solutions+Stadium,Piscataway,NJ&zoom=14&size=540x304&maptype=roadmap&markers=color:blue%7Clabel:S%7C40.511827,-74.462018&markers=color:red%7Clabel:C%7C40.514736,-74.478021'},
    {id: '2', name: "Nice run in Johnson Park", type: 'run', icon:'ion-ribbon-a', date: new Date("2015", "09", "25"), distance: 1.1, duration: 660.0, gmap: staticMap + '&path=40.511827,-74.462018|40.514736,-74.478021&center=Highpoint+Solutions+Stadium,Piscataway,NJ&zoom=14&size=540x304&maptype=roadmap&markers=color:blue%7Clabel:S%7C40.511827,-74.462018&markers=color:red%7Clabel:C%7C40.514736,-74.478021'},
    {id: '3', name: "Nice bike in Johnson Park", type: 'bike', icon:'ion-android-bicycle', date: new Date("2015", "09", "05"), distance: 1.1, duration: 420.0, gmap: staticMap + '&path=40.511827,-74.462018|40.514736,-74.478021&center=Highpoint+Solutions+Stadium,Piscataway,NJ&zoom=14&size=540x304&maptype=roadmap&markers=color:blue%7Clabel:S%7C40.511827,-74.462018&markers=color:red%7Clabel:C%7C40.514736,-74.478021'}
  ];
  */

})

.controller('FoodsCtrl', function($scope, $stateParams, AuthenticationService, FoodService) {
  $scope.username = AuthenticationService.CurrentUser().username;
  
  // Get the list of foods from the server for display purposes.
  FoodService.GetFoodList().then(function (response){
    if(response.success) {
      $scope.foods = response.data;
    }
  });

  // Get user's list of foods
  FoodService.GetAll($scope.username).then(function(response) {
    if(response.success) {
      $scope.foodList = response.data;
    }
  });


  $scope.formatDate = function(date) {
    if(date) {
      console.log(date);
      return moment(date).format('ll');
    }
  }

  $scope.formatCalories = function(calories) {
    if(calories) {
      var calculatedCalories = parseFloat(calories);
      var value = calculatedCalories.toFixed(2) + " calories";
      return value;
    }
  }

  $scope.getFoodIcon = function(foodName) {
    var foods = {
      'cheese pizza': 'ion-pizza',
      'coffee (milk and sugar)': 'ion-coffee',
      'yellow cake with vanilla frosting': 'ion-fork'
    };
    var retIcon = foods[foodName.toLowerCase()];
    return retIcon || 'ion-fork';
  }


  /*
  [
  {"food_id":1,"food_name":"Cheese Pizza","calories":272,"serving_size":"1 slice","serving_size_normalized":103},
  {"food_id":2,"food_name":"Coffee (milk and sugar)","calories":41,"serving_size":"8 fl oz","serving_size_normalized":237},
  {"food_id":3,"food_name":"Yellow Cake with Vanilla Frosting","calories":239,"serving_size":"1 slice(1\/8 of 18oz cake)","serving_size_normalized":64}
  ]

  {"userfood_id":"2",
  "food":"1",
  "serving":"2.50",
  "meal":"breakfast",
  "food_timestamp":"2015-11-23T14:34:43.954Z",
  "email":"ntaylor@aps.rutgers.edu",
  "food_name":"Cheese Pizza",
  "calories_per_serving":"272",
  "serving_size":"1 slice",
  "serving_size_normalized":103,
  "total_calories":680,
  "total_mass":257}
  */

  /*
  [
    {id: '1', type: 'lunch', food: 'pizza', icon:'ion-pizza', calories: 215, serving_label: 'Quick Snack', serving: '0.5', date: new Date("2015", "10", "02")},
    {id: '2', type: 'breakfast', food: 'coffee', icon:'ion-coffee', calories: 130, serving_label: 'A Lot', serving: '3', date: new Date("2015", "10", "02")},
    {id: '3', type: 'other', food: 'cake', icon:'ion-fork', calories: 600, serving_label: 'Normal', serving: '1', date: new Date("2015", "10", "02")}
  ];
  */

});
