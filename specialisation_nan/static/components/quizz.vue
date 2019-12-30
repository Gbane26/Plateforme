<template>
    <div class="h5 font-weight-normal one-slide mx-auto">
        <div class="testimonial  px-3 d-flex flex-direction-column justify-content-center flex-wrap ">
            <div>
                <span class="badge badge-secondary badge-question">Question 1</span>
                <br><br>
                <p class="quiz-question">
                    They’ve been consistent throughout 
                    the years and grown together with us. 
                    Even as they’ve grown, they haven’t lost 
                    sight of what they do. Most of their key 
                    resources are still with them, which is also 
                    a testament to their organization.
                </p>
                <br><hr><br>
                <div class="new">
                    <form>
                        <div class="form-groupe">
                            <input type="checkbox" id="html">
                            <label for="html">HTML</label>
                        </div>
                        <div class="form-groupe">
                            <input type="checkbox" id="css">
                            <label for="css">CSS</label>
                        </div>
                        <div class="form-groupe">
                            <input type="checkbox" id="javascript">
                            <label for="javascript">Javascript</label>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
    module.exports = {
        delimiters: ["${", "}"],
        mounted() {
            
        },
        methods: {
            login: function () {
                axios.defaults.xsrfCookieName = 'csrftoken'
                axios.defaults.xsrfHeaderName = 'X-CSRFToken'
                axios.post('http://127.0.0.1:8000/post', {
                    email: '' + this.email,
                    password: '' + this.password,
                }).then(response => {
                    console.log(response)
                    if (response.data.success) {
                        this.isSuccess = true
                        this.error = false
                        this.message = response.data.message
                        this.success = response.data.success
                        window.location.replace("home");
                    }
                    else {
                        this.error = true
                        this.message = response.data.message
                        this.success = response.data.success
                        this.isSuccess = false
                    }
                    console.log("success variable" + this.isSuccess)
                    // console.log("success variable"+this.error)
                })
                    .catch((err) => {
                        console.log(err);
                    })
            },
        }
    }
</script>