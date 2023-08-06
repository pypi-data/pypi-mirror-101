/*
The MIT License (MIT)

Copyright (c) 2015 University of East Anglia, Norwich, UK

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

Developed by Geoffrey French in collaboration with Dr. M. Fisher and
Dr. M. Mackiewicz.
 */
/// <reference path="./math_primitives.ts" />
/// <reference path="./abstract_label.ts" />
/// <reference path="./abstract_tool.ts" />
var labelling_tool;
(function (labelling_tool) {
    /*
    Undo-redo stack
     */
    var UndoRedoAction = /** @class */ (function () {
        function UndoRedoAction() {
        }
        return UndoRedoAction;
    }());
    var UndoRedoStack = /** @class */ (function () {
        function UndoRedoStack(max_size) {
            this.past = [];
            this.future = [];
            this.max_size = max_size;
        }
        UndoRedoStack.prototype.add_action = function (action) {
            this.past.push(action);
            while (this.past.length > this.max_size) {
                this.past.shift();
            }
            this.future = [];
        };
        UndoRedoStack.prototype.add_and_apply_action = function (action) {
            this.add_action(action);
            action.invoke();
        };
        UndoRedoStack.prototype.undo = function () {
            if (this.past.length > 0) {
                // Move the action from the past into the future
                var action = this.past.pop();
                this.future.push(action);
                // Revert
                action.revert();
                return action;
            }
            else {
                return null;
            }
        };
        UndoRedoStack.prototype.redo = function () {
            if (this.future.length > 0) {
                // Move the action from the future into the past
                var action = this.future.pop();
                this.past.push(action);
                // Invoke it
                action.invoke();
                return action;
            }
            else {
                return null;
            }
        };
        return UndoRedoStack;
    }());
    labelling_tool.UndoRedoStack = UndoRedoStack;
})(labelling_tool || (labelling_tool = {}));
//# sourceMappingURL=undo_redo.js.map