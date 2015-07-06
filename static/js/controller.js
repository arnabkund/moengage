
angular.module('app', ['ngRoute'])
  .controller('TodoController', ['$scope', '$location', '$http', '$rootScope', '$window', function ($scope, $location, $http, $rootScope, $window) {
     $rootScope.user = {};
     

  $window.fbAsyncInit = function() {
    FB.init({ 

      appId: '877885662248116', 

      channelUrl: 'app/channel.html', 

      status: true, 

      cookie: true, 

      xfbml: true,

      version: 'v2.3'
    });
    FB.getLoginStatus(function(response){
      console.log(response);
      if(response.status === 'connected')
      {
        $rootScope.getUserInfo();
      }
    });

  };

  (function(d){
    
    var js, 
    id = 'facebook-jssdk', 
    ref = d.getElementsByTagName('script')[0];

    if (d.getElementById(id)) {
      return;
    }

    js = d.createElement('script'); 
    js.id = id; 
    js.async = true;
    js.src = "http://connect.facebook.net/en_US/sdk.js";

    ref.parentNode.insertBefore(js, ref);

  }(document));

  $rootScope.watchLoginChange = function() {

    var _self = this;

    FB.Event.subscribe('auth.authResponseChange', function(res) {

      if (res.status === 'connected') {
        
       console.log(res);
        $rootScope.getUserInfo();

        
         // This is also the point where you should create a 
         // session for the current user.
         // For this purpose you can use the data inside the 
         // res.authResponse object.
        

      } 
      else {

        //$location.path("/");
         
      }

    });

  }
  $rootScope.getUserInfo = function() {

    var _self = this;

    FB.api('/me', function(res) {

      $rootScope.$apply(function() { 
        
        var n={};
        console.log(n);
        //console.log(JSON.stringify(res));
        FB.api('/me/friends', function(res1) {
          $rootScope.$apply(function() {
            res.friends=res1.data;
            
            for(friend in res.friends)
            { 
              var name="";
              var id="";
              for(oid in res.friends[friend])
              {
                if(oid=='name')
                  name=res.friends[friend][oid];
                if(oid=='id')
                  id=res.friends[friend][oid];
              }
              n[id]=name;
            }

            $rootScope.user = _self.user = res;
            console.log(n);
            $rootScope.friends_map = n;
            console.log(JSON.stringify(res));
            $http.post('http://localhost:5000/insert_user/',JSON.stringify(res)).
              success(function(data, status, headers, config) {
                console.log(data);
                $rootScope.feed_list=data;
                if(data.status === 'success')
                  $location.path('/feed')
                else
                  $scope.error=true;
              }).
              error(function(data, status, headers, config) {
                console.log(data);
                $scope.error=true;
              });
            // $location.path( "/feed" );
          });
        }); 
        
        

      });

    });

  };

  $rootScope.logout = function() {

    var _self = this;

    FB.logout(function(response) {

      $rootScope.$apply(function() { 

        $rootScope.user = _self.user = {}; 

      }); 

    });
  };
  }])
  
  .controller('TodoDetailCtrl', ['$http', '$location', '$scope', '$rootScope', '$routeParams', function ($http, $location, $scope, $rootScope, $routeParams) {
    
    //$rootScope.watchLoginChange();
    $scope.redirect=function(str){
        if(str=='home')
          $location.path( '/' );
        else
          $location.path( '/feed' );
      };
    if($rootScope.user === undefined)
    {
      $location.path( '/' );
    }
    else
    {
      

      console.log($scope.friends_map);
      $scope.user=$rootScope.user;
      $scope.feed_list=$rootScope.feed_list;
      $scope.friends_map = $rootScope.friends_map;
      $scope.friends_map[$rootScope.user.id]=$rootScope.user.name;
      $scope.img_url='graph.facebook.com/'+$rootScope.user.id+'/picture?type=small';
      console.log($scope.user.friends);
      $scope.map=function(id,event){
        console.log($scope.friends_map[id]);
        return ($scope.friends_map[id]);

      };
      $scope.redirect=function(str){
        if(str=='home')
          $location.path( '/' );
        else
          $location.path( '/posts' );
      };
      $scope.logout=$rootScope.logout;

      $scope.submit_comment=function(event){
        if(event.which==13)
        {
          console.log(event.currentTarget.value);
          $http.post('http://localhost:5000/insert_comment/',JSON.stringify({'user_name':$rootScope.user.name,'user_id':$rootScope.user.id,'author_id':event.currentTarget.attributes['data-aid'].value,'oid':event.currentTarget.attributes['data-oid'].value,'comment':event.currentTarget.value, 'created_at':event.currentTarget.attributes['data-at'].value})).
          success(function(data, status, headers, config) {
            if(data.status === 'success')
              $scope.feed_list=data;
              event.currentTarget.value='';
          }).
          error(function(data, status, headers, config) {
            
          });
        }
      };

      $scope.get_name=function(){
        console.log('da');
      };
    }

    

  }])

  .controller('postsCtrl', ['$http', '$location', '$scope', '$rootScope', '$routeParams', function ($http, $location, $scope, $rootScope, $routeParams) {
    if($rootScope.user === undefined)
    {
      $location.path( '/' );
    }
    else
    {
      $scope.redirect=function(str){
        if(str=='home')
          $location.path( '/' );
        else
          $location.path( '/feed' );
      };
      
      $scope.friends_map =$rootScope.friends_map;
      $scope.user=$rootScope.user;
      $scope.tag_friends={};
      $scope.tag_friends[$rootScope.user.id]=true;
      $scope.sho= function(){
        console.log($scope.tag_friends);
        $http.post('http://localhost:5000/insert_post/',JSON.stringify({'author_id':$rootScope.user.id,'author_name':$rootScope.user.name,'tag_list':$scope.tag_friends,'post_data':$scope.post_text})).
          success(function(data, status, headers, config) {
            if(data.status === 'success')
              {
                console.log('successful');
                $http.post('http://localhost:5000/insert_user/',JSON.stringify($rootScope.user)).
                  success(function(data, status, headers, config) {
                    $rootScope.feed_list=data;
                    if(data.status === 'success')
                      $location.path('/feed')
                    else
                      $scope.error=true;
                  }).
                  error(function(data, status, headers, config) {
                    console.log(data);
                    $scope.error=true;
                  });
                
              }
          }).
          error(function(data, status, headers, config) {
            
          });
      };
      $scope.img_url='graph.facebook.com/'+$rootScope.user.id+'/picture?type=small';
    }
    

  }])

  .config(['$routeProvider', function ($routeProvider) {
    $routeProvider
      .when('/', {
        templateUrl: '/todos.html',
        controller: 'TodoController'
      })
    
      .when('/feed', {
        templateUrl: '/todoDetails.html',
        controller: 'TodoDetailCtrl'
     })
      .when('/posts', {
        templateUrl: '/posts.html',
        controller: 'postsCtrl'
     });
  }])
  .config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');
  });
