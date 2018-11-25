import 'bootstrap';
import 'jquery';
import 'bootstrap/dist/css/bootstrap.min.css';
import './home.css';


console.log("Hello Dude");

var windowHeight = $(window).height();

console.log("Window height: ", windowHeight);

$("#content-area").height(windowHeight);