(function () {
  var SLIDES = {
    "Your dress": {
      src: "/videos/slide-1.mp4",
      label: "Abstract motion background",
    },
    "From data": {
      src: "/videos/slide-2.mp4",
      label: "Blue glass background",
    },
  };

  function makeVideo(alt, variant, src, label) {
    var video = document.createElement("video");
    video.setAttribute("playsinline", "");
    video.setAttribute("autoplay", "");
    video.setAttribute("muted", "");
    video.setAttribute("loop", "");
    video.setAttribute("preload", "metadata");
    video.setAttribute("src", src);
    video.setAttribute("aria-label", label);
    video.className =
      "Media-module-scss-module__lFYlva__" +
      variant +
      " FullSizeScrollerStepper-module-scss-module__K-7siW__media";
    return video;
  }

  function ensureSlideVideo(alt, info) {
    var selector =
      '[class*="FullSizeScrollerStepper"] [aria-label="' + info.label + '"],' +
      '[class*="FullSizeScrollerStepper"] img[alt="' + alt + '"]';

    document.querySelectorAll(selector).forEach(function (node) {
      var variant = "desktop";
      if (node.className && node.className.indexOf("__mobile") !== -1) {
        variant = "mobile";
      } else if (node.tagName === "IMG") {
        variant =
          node.className.indexOf("__mobile") !== -1 ? "mobile" : "desktop";
      }

      if (node.tagName === "VIDEO") {
        if (node.getAttribute("src") !== info.src) {
          node.setAttribute("src", info.src);
        }
        node.muted = true;
        node.loop = true;
        node.playsInline = true;
        if (node.paused) {
          node.play().catch(function () {});
        }
        return;
      }

      var video = makeVideo(alt, variant, info.src, info.label);
      node.replaceWith(video);
      video.play().catch(function () {});
    });
  }

  function fixScrollerMedia() {
    Object.keys(SLIDES).forEach(function (alt) {
      ensureSlideVideo(alt, SLIDES[alt]);
    });
  }

  fixScrollerMedia();

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", fixScrollerMedia);
  }

  window.addEventListener("load", fixScrollerMedia);

  var observer = new MutationObserver(fixScrollerMedia);
  observer.observe(document.documentElement, {
    childList: true,
    subtree: true,
    attributes: true,
    attributeFilter: ["src", "srcset"],
  });

  var intervalId = window.setInterval(fixScrollerMedia, 500);

  window.setTimeout(function () {
    observer.disconnect();
    window.clearInterval(intervalId);
  }, 10000);
})();
