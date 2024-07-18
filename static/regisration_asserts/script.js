let currentStep = 0;
const steps = document.querySelectorAll('.step');

function showStep(stepIndex) {
    steps.forEach((step, index) => {
        step.style.display = (index === stepIndex) ? 'block' : 'none';
    });
    // Show or hide navigation buttons based on the current step
    document.getElementById('prevBtn').style.display = (stepIndex === 0) ? 'none' : 'inline-block';
    document.getElementById('nextBtn').style.display = (stepIndex === steps.length - 1) ? 'none' : 'inline-block';
    document.getElementById('submitBtn').style.display = (stepIndex === steps.length - 1) ? 'inline-block' : 'none';
}

function nextStep() {
    if (currentStep < steps.length - 1) {
        const activeStep = steps[currentStep];
        // Run validations for the current step
        if (!validateCurrentStep(activeStep)) {
            return; // Stop execution if validation fails
            }
            currentStep++;
            showStep(currentStep);
        }
}

function prevStep() {
    if (currentStep > 0) {
        currentStep--;
        showStep(currentStep);
    }
}

function selectJlptLevel(level) {
    document.getElementById("jlpt_level").value = level;
    const buttons = document.querySelectorAll("#jlptLevelButtons .btn");
    buttons.forEach((button, index) => {
        button.classList.toggle("active", 5 - index === level);
    });
}

function validateCurrentStep(activeStep) {
    if (currentStep === 0) {
        const jlptLevel = document.getElementById("jlpt_level").value;
        if (jlptLevel < 1 || jlptLevel > 5) {
            Swal.fire({
                icon: 'error',
                title: 'Oops...',
                text: 'Please select a Valid JLPT Level!'
            });            return false;
        }
        const testCenter = document.getElementById("test_center").value;
        if (testCenter !== "Rabat") {
            Swal.fire({
                icon: 'error',
                title: 'Oops...',
                text: 'Please select a Valid Test Center!'
            });
            return false;
        }
    } else if (currentStep === 1) {
        const fullNameInput = activeStep.querySelector('#full_name');
        const fullName = fullNameInput.value;
        const pattern = /^[A-Za-z\s]+$/;
        if (!pattern.test(fullNameInput.value) || fullName.length < 3) {
            Swal.fire({
                icon: 'error',
                title: 'Oops...',
                text: 'Please enter a valid Given Name (letters and spaces only).'
            });
            return;
        }


    } else if (currentStep === 2) { // Assuming this is within a conditional block for step 2


            var dateString = $("#datepicker").val(); // Get the date as a string

            if (!dateString) {
                // If date is not selected or pass code validation fails, stop the form from proceeding
                Swal.fire({
                    icon: 'error',
                    title: 'Oops...',
                    text: 'Please select a valid birthday date.'
                });
                return false;
            } 
            
            const pass_code = document.getElementById("pass_code").value;
            const regex = /^\d{8}$/;
    
            if (!regex.test(pass_code)) {
                Swal.fire({
                    icon: 'error',
                    title: 'Oops...',
                    text: 'Please enter only 8 Digit code.'
                });
                    return false;
            }
            const confirm_pass_code = document.getElementById("confim_code").value; // Corrected typo
            if (pass_code !== confirm_pass_code) {
                Swal.fire({
                    icon: 'error',
                    title: 'Oops...',
                    text: 'Please enter the same code.'
                });
                    return false;
            }
            return true;

    } else if (currentStep === 3) { // Step 3: Native Language and Nationality
        const native_language = document.getElementById("native_language").value;
        if (![701, 606, 408, 411, 430, 112, 0].includes(parseInt(native_language))) {
            Swal.fire({
                icon: 'error',
                title: 'Oops...',
                text: 'Please enter the correct native language.'
            });
            return;
        }

        const nationalityInput = activeStep.querySelector('#nationality');
        if (!nationalityInput.value) {
            Swal.fire({
                icon: 'error',
                title: 'Oops...',
                text: 'Please select a valid nationality'
            });
            return;
        }

    } else if (currentStep === 4) { // Step 4: Address Information
        const addressInput = activeStep.querySelector('#adress');
        const addressvalue = addressInput.value;
        if (!addressInput.value || addressvalue.length < 5) {
            Swal.fire({
                icon: 'error',
                title: 'Oops...',
                text: 'Please enter a valid Adress.'
            });
            return;
        }

        const countrySelect = activeStep.querySelector('#countrySelect');
        const otherCountryInput = activeStep.querySelector('#otherCountry');
        if (countrySelect.value === "other" && !otherCountryInput.value) {
            Swal.fire({
                icon: 'error',
                title: 'Oops...',
                text: 'Please specify your country.'
            });
            return;
        }
    } else if (currentStep === 5) { // Step 5: ZIP Code, Phone Number, Email
        const zipCodeInput = activeStep.querySelector('#zip_code');
        const zipCodePattern = /^\d{5}$/; // Moroccan ZIP Code format
        if (!zipCodePattern.test(zipCodeInput.value)) {
            Swal.fire({
                icon: 'error',
                title: 'Oops...',
                text: 'Please enter a valid ZIP Code.'
            });
            return;
        }

        const phoneNumberInput = activeStep.querySelector('#phone_number');
        const phoneNumberPattern = /^(?:\+212|0)([ \-_/]*)(\d{9})$/; // Moroccan phone number format
        if (!phoneNumberPattern.test(phoneNumberInput.value)) {
            Swal.fire({
                icon: 'error',
                title: 'Oops...',
                text: 'Please enter a valid Phone Number.'
            });
            return;
        }

        const emailInput = activeStep.querySelector('#email');
        const confirmemailInput = activeStep.querySelector('#confirm_email');
        if (!emailInput.checkValidity()) {
            Swal.fire({
                icon: 'error',
                title: 'Oops...',
                text: 'Please enter a valid Email Adress.'
            });
            return;
        }
        if (emailInput.value !== confirmemailInput.value) {
            Swal.fire({
                icon: 'error',
                title: 'Oops...',
                text: 'Please enter the same email adress.'
            });
            return;
        }
    } else if (currentStep === 6) { // Step 6: Institute
        const instituteInput = activeStep.querySelector('#institute').value;
        if (!activeStep.querySelector("#institute").value || instituteInput.length < 3) {
            Swal.fire({
                icon: 'error',
                title: 'Oops...',
                text: 'Please enter a valid institute.'
            });
            return;
        }
        const placelearnngjp = activeStep.querySelector('#place_learn_jp').value;
        if (!placelearnngjp) {
            Swal.fire({
                icon: 'error',
                title: 'Oops...',
                text: 'Please select a valid Learning Place.'
            })
        }
    } else if (currentStep === 7) { // Step 7: Reason for Taking the Exam
        if (!activeStep.querySelector('#reason_jlpt').value) {
            Swal.fire({
                icon: 'error',
                title: 'Oops...',
                text: 'Please select a reason for taking the exam.'
            });
            return;
        }
        if (!activeStep.querySelector('#occupation').value) {
            Swal.fire({
                icon: 'error',
                title: 'Oops...',
                text: 'Please select an occupation.'
            });
            return;
        }
        if (!activeStep.querySelector('#occupation_details').value) {
            Swal.fire({
                icon: 'error',
                title: 'Oops...',
                text: 'Please select occupation details.'
            });
            return;
        }
    } else if( currentStep === 12) {
        if (!activeStep.querySelector('#paymentmethod').value) {
            Swal.fire({
                icon: 'error',
                title: 'Oops...',
                text: 'Please choose a Valid Payment Methode.'
            });
            return;
        }
    }
    currentStep++
    showStep(currentStep);
     // Initialize form by showing the first step
}
showStep(currentStep);


function filterNationality(event) {
    const input = event.target.value.toLowerCase();
    const options = document.querySelectorAll('#nationality option:not(:first-child)');

    options.forEach(option => {
        const optionText = option.textContent.toLowerCase();
        const optionValue = option.value.toLowerCase();
        if (optionText.includes(input) || optionValue.includes(input)) {
            option.style.display = 'block';
        } else {
            option.style.display = 'none';
        }
    });
}

function updateHiddenInputs(inputName, value) {
    // Check if the input already exists within the form
    var existingInput = $('#jlptform').find('input[name="' + inputName + '"]');
    
    if (existingInput.length > 0) {
        // If the input exists, update its value
        existingInput.val(value);
    } else {
        // If the input does not exist, append a new hidden input to the form
        $('#jlptform').append('<input type="hidden" name="' + inputName + '" value="' + value + '">');
    }
}