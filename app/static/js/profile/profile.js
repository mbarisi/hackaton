
$('#result').click(function() {
    var age = document.getElementById("age");
    var address = document.getElementById("address");
    var postcode_num = document.getElementById("postcode_num");
    var email_job = document.getElementById("email_job");
    var ageNum = parseInt(age.value);
    var addressNum = parseInt(address.value);
    var postcode_numNum = parseInt(postcode_num.value);
    var email_jobNum = parseInt(email_job.value);
    console.log(ageNum, addressNum, postcode_numNum, email_jobNum);

    if (!ageNum || age.value === "Enter your age here"){
        age.value = 0;
    }
    if (!addressNum || address.value === "Enter your address here"){
        address.value = 0;
    }
    if (!postcode_numNum || postcode_num.value === "Enter your postcode here"){
        age.value = 0;
    }
    if (!email_jobNum || email_job.value === "Enter email here"){
        age.value = 0;
    }
});
