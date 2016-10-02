/*var namestring = prompt("Enter a list of names seperated by spaces");
var names = namestring.split(" ");

function postData(input) {
    console.log("begin ajax call");
    $.ajax({
        type: 'GET',
        url: '/hello/',
        //data: {memes},
        success: function (newdata) {
		console.log("it worked!");
		console.log(newdata);
	}
    });
    console.log("end ajax call");
}


postData(names);*/

$.ajax({
	dataType: 'json',
	url: 'data.json',
	success: function (data) {
		console.log("data received");
		console.log("First node ID: " + data[0].sc_id);
		console.log("Mutual array length: " + data[0].mutuals.length);
		console.log("Mutual ID: " + data[0].mutuals[50])
		var graph = Viva.Graph.graph();
		for (x = 0; x < data.length-1; x++)
		{
			mutualfollow = data[x].mutuals.split(", ");
			mutualfollow = mutualfollow.slice(1,mutualfollow.length-2);
			graph.addNode(data[x].sc_id, {url : data[x].avatar_url});
			for (y = 0; y < mutualfollow.length; y++)
			{
				for (z = 0; z < data.length-1; z++)
				{
					if (mutualfollow[y] === data[z].sc_id.toString())
						graph.addLink(data[x].sc_id, data[y].sc_id);
				}
			}
		}
		
		// Set custom nodes appearance
		var graphics = Viva.Graph.View.svgGraphics();
		graphics.node(function(node) {
			if (node.links.length == 0)
				graph.removeNode(node.id);
			else {
				var relevance = 1;
				for (x = 0; x < data.length-1; x++)
					if (data[x].sc_id === node.id)
						relevance = data[x].relevancy;
      				// The function is called every time renderer needs a ui to display node
       				return Viva.Graph.svg('image')
        			     .attr('width', (240*relevance))
         			     .attr('height', (240*relevance))
 		        	     .link(node.data.url); // node.data holds custom object passed to graph.addNode();
    			}
		})
    		.placeNode(function(nodeUI, pos){
        		// Shift image to let links go to the center:
       			 nodeUI.attr('x', pos.x - 12).attr('y', pos.y - 12);
    		});

		var renderer = Viva.Graph.View.renderer(graph, {container: document.getElementById('graphDiv'),
		        updateCenterRequired: true,
       			graphics: graphics});
		renderer.run();	
	}
});

/*var graph = Viva.Graph.graph();

for (x = 0; x < names.length; x++)
{
	graph.addNode(names[x], {url : 'http://i0.kym-cdn.com/photos/images/original/000/927/630/798.png'});
	if (x != 0)
		graph.addLink(names[x], names[x-1]);
}

// Set custom nodes appearance
var graphics = Viva.Graph.View.svgGraphics();
graphics.node(function(node) {
       // The function is called every time renderer needs a ui to display node
       return Viva.Graph.svg('image')
             .attr('width', 24)
             .attr('height', 24)
             .link(node.data.url); // node.data holds custom object passed to graph.addNode();
    })
    .placeNode(function(nodeUI, pos){
        // Shift image to let links go to the center:
        nodeUI.attr('x', pos.x - 12).attr('y', pos.y - 12);
    });

var renderer = Viva.Graph.View.renderer(graph, {container: document.getElementById('graphDiv'),
	updateCenterRequired: true,
	graphics: graphics});
renderer.run();

var layout = Viva.Graph.Layout.constant(graph);
graph.forEachNode(function(node){
	console.log(layout.getNodePosition(node.id));
})*/
