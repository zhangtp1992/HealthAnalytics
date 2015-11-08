/**
 * Created by willkara on 10/28/15.
 */
$(document).ready(function () {
    $('ul.exportlist li').click(function (e) {
        alert('EXPORTED');
    });


});

var map;
var commMap;

function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: 40.504022, lng: -74.452681},
        zoom: 14
    });

    var start = new google.maps.Marker({
        position: {lat: 40.504022, lng: -74.452681},
        map: map,
        title: 'Start',
        label: 'Start'
    });


    var mile1 = new google.maps.Marker({
        position: {lat: 40.508318, lng: -74.467134},
        map: map,
        title: 'Mile 1',
        label: '1'
    });

    //Create the first infowindow
    var mile1content = '<div id="content"><h1>Split: 6.30</h1></div>';
    var mile1info = new google.maps.InfoWindow({
        content: mile1content
    });

    //Open the first info window
    google.maps.event.addListener(mile1, 'click', function () {
        mile1info.open(map, mile1);
    });


    var mile2 = new google.maps.Marker({
        position: {lat: 40.51371914911811, lng: -74.48497640016782},
        map: map,
        title: 'Mile 2',
        label: '2'
    });

    //Create the second info window
    var mile2contentSplit = '<div id="content"><h1>Split 7.00</h1></div>';
    var mile2contentTotal = '<div id="content"><h1>Total Time: 13.30</h1></div>';
    var mile2Info = new google.maps.InfoWindow({
        content: mile2contentSplit + mile2contentTotal
    });

    //Open the second info window
    google.maps.event.addListener(mile2, 'click', function () {
        mile2Info.open(map, mile2);
    });

    var mile3 = new google.maps.Marker({
        position: {lat: 40.52681900281688, lng: -74.49428040526213},
        map: map,
        title: 'Mile 3',
        label: '3'
    });


    var demoPathCords = [
        {lat: 40.5040307735982, lng: -74.4527209795127},
        {lat: 40.5059265217711, lng: -74.4547243359951},
        {lat: 40.5040761483921, lng: -74.4577674161866},
        {lat: 40.5055976434702, lng: -74.4606001158881},
        {lat: 40.5067088938651, lng: -74.4605031011393},
        {lat: 40.5074086299421, lng: -74.461258850648},
        {lat: 40.50768992831, lng: -74.4639853539422},
        {lat: 40.5079943217216, lng: -74.4640260384159},
        {lat: 40.508300645151, lng: -74.467077497999},
        {lat: 40.5083091422835, lng: -74.4671179631525},
        {lat: 40.5101258400497, lng: -74.4743710475033},
        {lat: 40.5103927385555, lng: -74.478829945172},
        {lat: 40.5118237999443, lng: -74.4829418524528},
        {lat: 40.5137663555899, lng: -74.4850459652522},
        {lat: 40.5137668289887, lng: -74.4850943233255},
        {lat: 40.5269937937022, lng: -74.4943083641602}
    ];

    var demoPath = new google.maps.Polyline({
        path: demoPathCords,
        map: map,
        geodesic: true,
        strokeColor: '#FF0000',
        strokeOpacity: 1.0,
        strokeWeight: 2
    });


    commMap = new google.maps.Map(document.getElementById('commMap'), {
        center: {lat: 40.504022, lng: -74.452681},
        zoom: 14
    });

    var p1 = new google.maps.Marker({
        position: {lat: 40.514088, lng: -74.452901},
        map: map,
        title: 'Run',
        label: 'Run'
    });

    var p2 = new google.maps.Marker({
        position: {lat: 40.504622, lng: -74.452081},
        map: map,
        title: 'Run',
        label: 'Run'
    });

    var p3 = new google.maps.Marker({
        position: {lat: 40.578022, lng: -74.454081},
        map: map,
        title: 'Run',
        label: 'Run'
    });

    var p4 = new google.maps.Marker({
        position: {lat: 40.504672, lng: -74.450081},
        map: map,
        title: 'Run',
        label: 'Run'
    });

    var p5 = new google.maps.Marker({
        position: {lat: 40.604022, lng: -74.452681},
        map: map,
        title: 'Run',
        label: 'Run'
    });
}

