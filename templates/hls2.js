<script src="https://cdn.jsdelivr.net/npm/hls.js@latest"></script>

<video id="video" width=100% height=100%></video>
<script>
  if (Hls.isSupported()) {
    var video = document.getElementById('video');
    var hls = new Hls();
    // bind them together
    hls.attachMedia(video);
    hls.on(Hls.Events.MEDIA_ATTACHED, function () {
      console.log('video and hls.js are now bound together !');
      hls.loadSource({{url }});
      hls.on(Hls.Events.MANIFEST_PARSED, function (event, data) {
        console.log(
          'manifest loaded, found ' + data.levels.length + ' quality level'
        );
      });
    });
  }
</script>
