var resume = document.getElementById("resume");
resume.onchange = function() {
    if(resume.files.length > 0)
        document.getElementById('file-label').innerHTML = resume.files[0].name;
};

