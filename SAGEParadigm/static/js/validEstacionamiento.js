$(function(){
	$('[data-toggle="popover"]').popover({
        trigger: 'manual',
        'placement': 'left',
        container: 'body',
        'show': true
    });
	
	$('#id_propietario').keyup(function(){
		var _this = $('#id_propietario');
		var _valor = $('#id_propietario').val();
		var regEx = /^[a-zA-ZáéíóúñÑÁÉÍÓÚüÜ][a-zA-ZáéíóúñÑÁÉÍÓÚüÜ ]*$/;
		var valid = regEx.test(_valor);
		var tam = _valor.length;
		
		if (valid && tam <= 50){
			_this.popover('hide');
		} else {
			_this.popover('show');
		}
		
	});
	
	$('#id_rif').keyup(function(){
		var _this = $('#id_rif');
		var _valor = $('#id_rif').val();
		var regEx = /^[JVD]-\d{8}-\d$/;
		var valid = regEx.test(_valor);
		
		if (valid){
			_this.popover('hide');
		} else {
			_this.popover('show');
		}
		
	});
	
	$('#id_telefono_1').keyup(function(){
		var _this = $('#id_telefono_1');
		var _valor = $('#id_telefono_1').val();
		var regEx = /^((0212)|(0412)|(0416)|(0414)|(0424)|(0426))-\d{7}$/;
		var valid = regEx.test(_valor);
		
		if (valid || _valor==""){
			_this.popover('hide');
		} else {
			_this.popover('show');
		}
		
	});
	
	$('#id_telefono_2').keyup(function(){
		var _this = $('#id_telefono_2');
		var _valor = $('#id_telefono_2').val();
		var regEx = /^((0212)|(0412)|(0416)|(0414)|(0424)|(0426))-\d{7}$/;
		var valid = regEx.test(_valor);
		
		if (valid || _valor==""){
			_this.popover('hide');
		} else {
			_this.popover('show');
		}
		
	});
	
	$('#id_telefono_3').keyup(function(){
		var _this = $('#id_telefono_3');
		var _valor = $('#id_telefono_3').val();
		var regEx = /^((0212)|(0412)|(0416)|(0414)|(0424)|(0426))-\d{7}$/;
		var valid = regEx.test(_valor);
		
		if (valid || _valor==""){
			_this.popover('hide');
		} else {
			_this.popover('show');
		}
		
	});
	
	$('#id_email_1').keyup(function(){
		var _this = $('#id_email_1');
		var _valor = $('#id_email_1').val();
		var regEx = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,4})+$/;
		var valid = regEx.test(_valor);
		
		if (valid || _valor==""){
			_this.popover('hide');
		} else {
			_this.popover('show');
		}
		
	});
	
	$('#id_email_2').keyup(function(){
		var _this = $('#id_email_2');
		var _valor = $('#id_email_2').val();
		var regEx = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,4})+$/;
		var valid = regEx.test(_valor);
		
		if (valid || _valor==""){
			_this.popover('hide');
		} else {
			_this.popover('show');
		}
		
	});
	
});
