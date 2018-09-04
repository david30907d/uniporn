var openFile = function(event) {
	var input = event.target; // target會抓到觸發openFile function的整行tag
	// console.log(input);
	// console.log(input.files);
	// console.log(input.files[0]);
	var reader = new FileReader();
	reader.readAsDataURL(input.files[0]);
	reader.onload = function(){
		var dataURL = reader.result;
		var output = document.getElementById('output');
		output.src = dataURL;
	};
};
