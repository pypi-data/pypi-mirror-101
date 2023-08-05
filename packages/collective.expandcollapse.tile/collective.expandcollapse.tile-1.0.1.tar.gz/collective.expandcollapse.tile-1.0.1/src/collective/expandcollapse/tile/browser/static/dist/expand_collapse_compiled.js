"use strict";

require(["jquery"], function ($) {
  "use strict";

  $(document).on("click", ".tile-collapse-button", function (e) {
    var collapse = $(e.target).closest(".collapsible, .collapsible-desktop");

    if (collapse.hasClass("accordion")) {
      $(".collapsible, .collapsible-desktop").each(function () {
        if (!$(this).is(collapse)) {
          $(this).removeClass("open");
          $(this).find(".tileBody, .tileContent").slideUp();
        }
      });
    }

    collapse.toggleClass("open");
    collapse.find(".tileBody, .tileContent").slideToggle();
  });

  function addButton(selector) {
    var titleDOM = $(selector).find("h2.tileTitle");
    titleDOM.each(function () {
      if ($(this).children("a").length === 0) {
        var title = $(this).text();
        var collapsible = $(this).closest(".collapsible, .collapsible-desktop");
        $(this).html('<a class="tile-collapse-button"><span class="title-content">'.concat(title).concat('</span><span class="title-icon"><i class="fas fa-angle-down"></i><i class="fas fa-angle-up"></i></span></a>'));

        if ($(collapsible).hasClass("default-open")) {
          $(collapsible).addClass("open");
        }
      }
    });
  }

  function removeButton(selector) {
    var titleDOM = $(selector).find("h2.tileTitle");
    titleDOM.each(function () {
      if ($(this).children("a").length > 0) {
        var title = $(this).text();
        $(this).html(title);
      }
    });
  }

  function handleTileCollapse() {
    if ($(".tileWrapper > .collapsible-desktop").length) {
      addButton(".tileWrapper > .collapsible-desktop");
    }

    if ($(".tileWrapper > .collapsible").length) {
      if (window.innerWidth <= 991) {
        addButton(".tileWrapper > .collapsible");
      } else {
        removeButton(".tileWrapper > .collapsible");
      }
    }
  }

  $(window).on("resize orientationchange", function () {
    handleTileCollapse();
  });
  $(function () {
    handleTileCollapse(); // browser has MutationObserver support

    if (window.MutationObserver) {
      // https://developer.mozilla.org/it/docs/Web/API/MutationObserver
      // Select the node that will be observed for mutations
      $(".pat-tiles-management").each(function () {
        // Options for the observer (which mutations to observe)
        var config = {
          attributes: false,
          childList: true,
          subtree: true
        }; // Callback function to execute when mutations are observed

        var callback = function callback(mutationsList, observer) {
          mutationsList.forEach(function (mutation) {
            if (mutation.type == "childList") {
              handleTileCollapse();
            }
          });
        }; // Create an observer instance linked to the callback function


        var observer = new MutationObserver(callback); // Start observing the target node for configured mutations

        observer.observe(this, config);
      });
    } else {
      // browser has no MutationObserver support
      $(".pat-tiles-management").on("rtTilesLoaded", function () {
        handleTileCollapse();
      });
    }
  });
});

define("src/collective/expandcollapse/tile/browser/static/expand_collapse.js", function () {});
//# sourceMappingURL=expand_collapse_compiled.js.map
