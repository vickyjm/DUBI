$(function(){
	$('[data-toggle="popover"]').popover({
        trigger: 'manual',
        'placement': 'left',
        container: 'body',
        'show': true
    });
	
	$('#id_fechaInicio').keyup(function(){
		var _this = $('#id_fechaInicio');
		var _valor = $('#id_fechaInicio').val();
		var regEx = /^\d{1,4}-(0?[1-9]|1[0-2])-([1-2][0-9]|3[0-1]|0?[1-9])$/;
		var valid = regEx.test(_valor);
		
		if (valid){
			_this.popover('hide');
		} else {
			_this.popover('show');
		}
		
	});
	
	$('#id_horaInicio').keyup(function(){
		var _this = $('#id_horaInicio');
		var _valor = $('#id_horaInicio').val();
		var regEx = /^([0-9]|[0-1][0-9]|2[0-3]):[0-5][0-9]$/;
		var valid = regEx.test(_valor);
		
		if (valid){
			_this.popover('hide');
		} else {
			_this.popover('show');
		}
		
	});
	
	$('#id_fechaFinal').keyup(function(){
		var _this = $('#id_fechaFinal');
		var _valor = $('#id_fechaFinal').val();
		var regEx = /^\d{1,4}-(0?[1-9]|1[0-2])-([1-2][0-9]|3[0-1]|0?[1-9])$/;
		var valid = regEx.test(_valor);

        
		if (valid){
			_this.popover('hide');
		} else {
			_this.popover('show');
		} 
	});
	
	$('#id_horaFinal').keyup(function(){
		var _this = $('#id_horaFinal');
		var _valor = $('#id_horaFinal').val();
		var regEx = /^([0-9]|[0-1][0-9]|2[0-3]):[0-5][0-9]$/;
		var valid = regEx.test(_valor);
		
		if (valid){
			_this.popover('hide');
		} else {
			_this.popover('show');
		}
		
	});
	
});
