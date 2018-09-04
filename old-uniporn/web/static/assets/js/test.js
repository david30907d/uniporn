// $(document).ready(function(){
//   $('form input').change(function () {
//     $('form p').text(this.files.length + " file(s) selected");
//   });
// });


var openFile = function(event) {
	var input = event.target;

	var reader = new FileReader();
	reader.onload = function(){
		var dataURL = reader.result;
		var output = document.getElementById('output');
		output.src = dataURL;
	};
	reader.readAsDataURL(input.files[0]);
};
