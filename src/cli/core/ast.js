export class Node { constructor(type) { this.type = type; } }
export class NodeVariable extends Node { constructor(name, value) { super('Variable'); this.name = name; this.value = value; } }
export class NodeFunction extends Node { constructor(name, params, body) { super('Function'); this.name = name; this.params = params; this.body = body; } }
export class NodeIf extends Node { constructor(cond, then, elsePart) { super('If'); this.cond = cond; this.then = then; this.elsePart = elsePart; } }
export class NodeAssignment extends Node { constructor(name, value) { super('Assignment'); this.name = name; this.value = value; } }
export class NodeCall extends Node { constructor(name, args) { super('Call'); this.name = name; this.args = args; } }
