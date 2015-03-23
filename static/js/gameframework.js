"use strict";
var GameFramework = (function () {
    function State(scene) {
        this.scene = scene;
    }

    State.prototype.destroy = function() {

    }

    State.prototype.reset = function() {

    }

    State.prototype.update = function(delta) {
        if(this.scene) {
            this.scene.update(delta);
        }
    }

    State.prototype.draw = function() {

    }

    State.prototype.keyPress = function(e) {

    }

    State.prototype.keyDown = function(e) {

    }

    State.prototype.focus = function(dom) {
      var that = this;
      dom.keypress(function(e) {
        that.keyPress(e);
      });
      dom.keydown(function(e) {
        that.keyDown(e);
      });
    }

    State.prototype.blur = function() {

    }


    function Framework(root) {
        this.root_dom = $(root);
        this.states = [];
        this.states.push(new State());
        this.active = false;
        this.last_update = Date.now();
    }

    Framework.prototype.update = function(delta) {
        if(this.active === true) {
            var that = this;
            window.requestAnimationFrame(function() {
                var new_delta = (Date.now() - that.last_update) / 1000;
                that.last_update = Date.now();
                that.update(new_delta);
            });
        }

        var state = this.states[this.states.length - 1];
        state.update(delta);
        state.draw();
    }

    Framework.prototype.start = function() {
        this.active = true;
        this.update(0);
    }

    Framework.prototype.resetState = function() {
        this.states[this.states.length - 1].reset();
    }

    Framework.prototype.pushState = function(state) {
        this.states[this.states.length - 1].blur();
        state.focus(this.root_dom);
        state.framework = this;
        this.states.push(state);
    }

    Framework.prototype.popState = function() {
        if(this.states.length > 1) {
            this.states[this.states.length - 1].blur();
            this.states[this.states.length - 1].destroy();
            this.states.pop();
            this.states[this.states.length - 1].focus(this.root_dom);
        }
    }

    var gameframework = {};
    gameframework.State = State;
    gameframework.Framework = Framework;
    return gameframework;
})();