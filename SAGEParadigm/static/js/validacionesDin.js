$(function(){
	$('[data-toggle="popover"]').popover({
        trigger: 'manual',
        'placement': 'right',
        container: 'body',
        'show': true
    });
	
	$('#id_nombre').keyup(function(){
		var _this = $('#id_nombre');
		var _valor = $('#id_nombre').val();
		var regEx = /^[a-zA-ZáéíóúñÑÁÉÍÓÚüÜ][a-zA-ZáéíóúñÑÁÉÍÓÚüÜ ]*$/;
		var valid = regEx.test(_valor);
		
		if (valid){
			$('#id_nombre').popover('hide');
		} else {
			$('#id_nombre').popover('show');
		}
		
	});
	
	$('#id_apellidos').keyup(function(){
		var _this = $('#id_apellidos');
		var _valor = $('#id_apellidos').val();
		var regEx = /^[a-zA-ZáéíóúñÑÁÉÍÓÚüÜ][a-zA-ZáéíóúñÑÁÉÍÓÚüÜ ]*$/;
		var valid = regEx.test(_valor);
		
		if (valid){
			$('#id_apellidos').popover('hide');
		} else {
			$('#id_apellidos').popover('show');
		}
		
	});
	
	$('#id_cedula').keyup(function(){
		var _this = $('#id_cedula');
		var _valor = $('#id_cedula').val();
		var regEx = /^([1-9][0-9]{0,3})(\.?[0-9]{3}){0,2}$/;
		var valid = regEx.test(_valor);

        
		if (valid){
			$('#id_cedula').popover('hide');
		} else {
			$('#id_cedula').popover('show');
		} 
	});
	
	$('#id_numTarjeta').keyup(function(){
		var _this = $('#id_numTarjeta');
		var _valor = $('#id_numTarjeta').val();
		var regEx = /^\d{4}-?\d{4}-?\d{4}-?\d{4}$/;
		var valid = regEx.test(_valor);
		
		if (valid){
			$('#id_numTarjeta').popover('hide');
		} else {
			$('#id_numTarjeta').popover('show');
		}
		
	});
	
});
