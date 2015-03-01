$(function(){
	$('[data-toggle="popover"]').popover({
        trigger: 'manual',
        'placement': 'left',
        container: 'body',
        'show': true
    });
	
	$('#id_puestos').keyup(function(){
		var _this = $('#id_puestos');
		var _valor = $('#id_puestos').val();
		var regEx = /^\d+$/;
		var valid = regEx.test(_valor);
		
		if (valid){
			_this.popover('hide');
		} else {
			_this.popover('show');
		}
		
	});
	
	$('#id_horarioin').keyup(function(){
		var _this = $('#id_horarioin');
		var _valor = $('#id_horarioin').val();
		var regEx = /^([0-9]|[0-1][0-9]|2[0-3]):[0-5][0-9]$/;
		var valid = regEx.test(_valor);
		
		if (valid){
			_this.popover('hide');
		} else {
			_this.popover('show');
		}
		
	});
	
	$('#id_horarioout').keyup(function(){
		var _this = $('#id_horarioout');
		var _valor = $('#id_horarioout').val();
		var regEx = /^([0-9]|[0-1][0-9]|2[0-3]):[0-5][0-9]$/;
		var valid = regEx.test(_valor);
		
		if (valid){
			_this.popover('hide');
		} else {
			_this.popover('show');
		}
		
	});
	
	$('#id_tarifa').keyup(function(){
		var _this = $('#id_tarifa');
		var _valor = $('#id_tarifa').val();
		var regEx = /^\d+(\.\d{1,2})?$/;
		var valid = regEx.test(_valor);
		
		if (valid){
			_this.popover('hide');
		} else {
			_this.popover('show');
		}
		
	});
	
	$('#id_hora_picoini').keyup(function(){
		var _this = $('#id_hora_picoini');
		var _valor = $('#id_hora_picoini').val();
		var regEx = /^([0-9]|[0-1][0-9]|2[0-3]):[0-5][0-9]$/;
		var valid = regEx.test(_valor);
		
		if (valid){
			_this.popover('hide');
		} else {
			_this.popover('show');
		}
		
	});
	
	$('#id_hora_picofin').keyup(function(){
		var _this = $('#id_hora_picofin');
		var _valor = $('#id_hora_picofin').val();
		var regEx = /^([0-9]|[0-1][0-9]|2[0-3]):[0-5][0-9]$/;
		var valid = regEx.test(_valor);
		
		if (valid){
			_this.popover('hide');
		} else {
			_this.popover('show');
		}
		
	});
	
	$('#id_tarifa_pico').keyup(function(){
		var _this = $('#id_tarifa_pico');
		var _valor = $('#id_tarifa_pico').val();
		var regEx = /^\d+(\.\d{1,2})?$/;
		var valid = regEx.test(_valor);
		
		if (valid){
			_this.popover('hide');
		} else {
			_this.popover('show');
		}
		
	});
	
	$('#id_tarifa_fin').keyup(function(){
		var _this = $('#id_tarifa_fin');
		var _valor = $('#id_tarifa_fin').val();
		var regEx = /^\d+(\.\d{1,2})?$/;
		var valid = regEx.test(_valor);
		
		if (valid){
			_this.popover('hide');
		} else {
			_this.popover('show');
		}
		
	});
	
});
