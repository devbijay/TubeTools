search_btn.addEventListener("click", function() {

var yt_url = document.getElementById("yt_url").value;
const div_el = document.getElementById("show_yt_img");
const search_btn = document.getElementById("search_btn");
hd_img = document.getElementById("hd_img");
sd_img = document.getElementById("sd_img");
normal_img1 = document.getElementById("normal_img1");
normal_img2 = document.getElementById("normal_img2");
normal_img3 = document.getElementById("normal_img3");

hd_img_btn = document.getElementById("hd_img_btn");
sd_img_btn = document.getElementById("sd_img_btn");
normal_img_btn = document.getElementById("normal_img_btn");
normal2_img_btn = document.getElementById("normal2_img_btn");
normal3_img_btn = document.getElementById("normal3_img_btn");

const res = yt_url.match(/(?:https?:\/{2})?(?:w{3}\.)?youtu(?:be)?\.(?:com|be)(?:\/watch\?v=|\/)([^\s&]+)/)
if (res == undefined) {
  alert("Please check the URL you have entered");
}
const videoId = res[1];
console.log(videoId);
base_url = "https://img.youtube.com/vi/"

hd_img.src = base_url + videoId+"/maxresdefault.jpg"
hd_img_btn.setAttribute('onclick', 'downloadImage("' + hd_img.src + '")');


sd_img.src = base_url + videoId+"/sddefault.jpg"
sd_img_btn.setAttribute('onclick', 'downloadImage("' + sd_img.src + '")');


normal_img1.src = base_url + videoId+"/hqdefault.jpg"
normal_img_btn.setAttribute('onclick', 'downloadImage("' + normal_img1.src + '")');

normal_img2.src = base_url + videoId+"/mqdefault.jpg"
normal2_img_btn.setAttribute('onclick', 'downloadImage("' + normal_img2.src + '")');


normal_img3.src = base_url + videoId+"/default.jpg"
normal3_img_btn.setAttribute('onclick', 'downloadImage("' + normal_img3.src + '")');

div_el.classList.remove("d-none");
});

  function downloadImage(url) {
  // const proxyUrl = 'https://cors-anywhere.herokuapp.com/';
  const imageUrl = url;
  fetch(imageUrl)
    .then(response => response.blob())
    .then(blob => {
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.style.display = 'none';
      a.href = url;
      a.download = 'image.jpg';
      a.click();
    });
}

