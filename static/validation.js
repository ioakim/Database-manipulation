$(document).ready(function() {
    // Get a specific form when it's about to be submitted
    $('#addCategory').submit(function(){
        var validIn = 0;
        // Get all inputs which accept text
        var allInputs = $(this).find(":text");
        // loops over them
        allInputs.each(function(){
            // Validate the values according to the database
            switch ($(this).attr('name')){//switch between the name of the fields
                case ('categoryID'):
                    if ($.isNumeric($(this).val())){
                        if ($(this).next().attr('class') == 'error')
                            //if there is an error message it removes it
							$(this).next().remove();
                        validIn++;//increases the number of valid inputs
                    }
                    else{
						$(this).next().remove();
                        $(this).after("<b class='error'>This input requires a number as the CategoryID<br/></b> ");
                    }
                    break;
                case ('name'):
                    if ($(this).val().length > 0 && $(this).val().length <= 50 && (this).val() != ''){
                        if ($(this).next().attr('class') == 'error')
                            $(this).next().remove();
                        validIn++;
                    }
                    else{
						$(this).next().remove();
						$(this).after("<b class='error'>This input can't be longer than 50 characters or empty<br/></b> ");}
                    break;
                default:
                    event.preventDefault();
            }
        });
        // If all the inputs are valid it accepts the form
        if (validIn == 2){
            return true;
        } else {
            event.preventDefault();
        }
    });

    $('#deleteCategory').submit(function(){
        // Find the input of type text we are going to use
        var categID = $(this).find(':text');
            if ($.isNumeric(categID.val())){
                if (categID.next().attr('class') == 'error')
                    categID.next().remove();
                return true;
            }
            else{
                categID.next().remove();
				categID.after("<b class='error'>This input requires a number for the categoryID to be deleted<br/></b> ");
                event.preventDefault();
            }
    });
	
	$('#reportPublisher').submit(function(){
        var pbName = $(this).find(':text');
            if (pbName.val().length > 0 && pbName.val().length <= 50 && pbName.val() != ''){
                        if (pbName.next().attr('class') == 'error')
                            pbName.next().remove();
                        return true;
            }
            else{
				pbName.next().remove();
				pbName.after("<b class='error'>This input can't be longer than 50 characters or empty<br/></b> ");
                event.preventDefault();
            }
    });
	
    $('#reportBook').submit(function(){
        var bookID = $(this).find(':text');
            if ($.isNumeric(bookID.val())){
                if (bookID.next().attr('class') == 'error')
                    bookID.next().remove();
                return true;
            }
            else{
				bookID.next().remove();
				bookID.after("<b class='error'>This input requires a number for the bookID<br/></b> ");
                event.preventDefault();
            }
    });

    $('#salesRepPerformance').submit(function(){
        var dateIn = new RegExp("^([0-9]{4})-([0-9]{2})-([0-9]{2})$");
        var validIn = 0;
        var allInputs = $("input[type = 'date']");

        allInputs.each(function(){
            console.log(dateIn.test($(this).val()));
            console.log($(this).val());
            if (dateIn.test($(this).val())){
                if ($(this).next().attr('class') == 'error')
                    $(this).next().remove();
                validIn++;
            } else {
				$(this).next().remove();
				$(this).after("<b class='error'>This date is in the wrong format<br/></b> ");
                event.preventDefault();
                return false;
            }
        });
        if (validIn == 2)
            return true;
        else
            event.preventDefault();
    });
		
	$('#discountCategory').submit(function(){
        var validIn = 0;
        // Get all inputs which accept text
        var allInputs = $(this).find(":text");
        // loops over them
        allInputs.each(function(){
            // Validate the values according to the database
            switch ($(this).attr('name')){//switch between the name of the fields
                case ('categoryID'):
                    if ($.isNumeric($(this).val())){
                        if ($(this).next().attr('class') == 'error')
                            //if there is an error message it removes it
							$(this).next().remove();
                        validIn++;//increases the number of valid inputs
                    }
                    else{
						$(this).next().remove();
						$(this).after("<b class='error'>This input requires a number as the CategoryID<br/></b>");
						event.preventDefault();
						
                    }
                    break;
                case ('discount'):
                    if ($.isNumeric($(this).val())){
                        if ($(this).next().attr('class') == 'error')
                            //if there is an error message it removes it
							$(this).next().remove();
                        validIn++;//increases the number of valid inputs
                    }
                    else{
						$(this).next().remove();
						$(this).after("<b class='error'>This input requires a number representing the discount<br/></b>");
                    }
                    break;
                default:
                    event.preventDefault();
            }
        });	
	});
});