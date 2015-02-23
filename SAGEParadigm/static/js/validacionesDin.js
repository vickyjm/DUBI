$(function(){
	$('#id_cedula').keyup(function(){
		var _this = $('#id_cedula');
		var _valor = $('#id_cedula').val();
		var regEx = /^([1-9][0-9]{0,3})(\.?[0-9]{3}){0,2}$/;
		var valid = regEx.test(_valor)
        
		if (valid){
			_this.attr('style', 'background:white');
		} else {
			_this.attr('style', 'background:#FF4A4A');
		}
	});

	$('#id_nombre').keyup(function(){
		var _this = $('#id_nombre');
		var _valor = $('#id_nombre');
		var regEx = /^[a-zA-ZáéíóúñÑÁÉÍÓÚüÜ][a-zA-ZáéíóúñÑÁÉÍÓÚüÜ ]*$/;
		var valid = regEx.test(_valor)
		
		if (valid){
			_this.attr('style', 'background:white');
		} else {
			_this.attr('style', 'background:#FF4A4A');
		}
		
	});
	
	$('#id_apellidos').keyup(function(){
		var _this = $('#id_apellidos');
		var _valor = $('#id_apellidos');
		var regEx = /^[a-zA-ZáéíóúñÑÁÉÍÓÚüÜ][a-zA-ZáéíóúñÑÁÉÍÓÚüÜ ]*$/;
		var valid = regEx.test(_valor)
		
		if (valid){
			_this.attr('style', 'background:white');
		} else {
			_this.attr('style', 'background:#FF4A4A');
		}
		
	});
	
	$('#id_numTarjeta').keyup(function(){
		var _this = $('#id_numTarjeta');
		var _valor = $('#id_numTarjeta');
		var regEx = /^\d{4}-?\d{4}-?\d{4}-?\d{4}$/;
		var valid = regEx.test(_valor)
		
		if (valid){
			_this.attr('style', 'background:white');
		} else {
			_this.attr('style', 'background:#FF4A4A');
		}
		
	});
	
});
