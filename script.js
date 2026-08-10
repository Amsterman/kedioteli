
document.querySelectorAll('[data-wa]').forEach(function(el){
  el.addEventListener('click',function(){
    const msg=el.getAttribute('data-wa')||'Merhaba, kedi bakımı hakkında bilgi almak istiyorum.';
    window.open('https://wa.me/905354315062?text='+encodeURIComponent(msg),'_blank');
  });
});
