// for the first initialization
$('document').ready(function () {

    $("#addButton").click(function () {
        $("#addButton").attr("disabled", true);
        const start = val_or_placeholder("#start_field");
        const end = val_or_placeholder("#end_field");
        const language = val_or_placeholder("#language_field");
        addPath(start, end, language);
    });

    $("#expandButton").click(function () {
        expandAll(tree_root);
        outer_update(tree_root);
    });

    $("#end_field,#language_field").on("change", function () {
        $("#tree-container").empty();
        draw_tree("",{"name":val_or_placeholder("#end_field"),"_children": [],});
        $('#searchSelect').empty();
    });

    
    $('#searchSelect').on('change', function() {
        clearAll(tree_root);
        expandAll(tree_root);
        outer_update(tree_root);

        searchText = $(this).val();
        searchTree(tree_root,true)
        tree_root.children.forEach(collapseAllNotFound);
        outer_update(tree_root);
        tree_root.children.forEach(centerSearchTarget);

    });
    const root = {
          "name": "Philosophy",
           "_children": [],
        } 
    draw_tree("",root);
});

function addPath(start,end,language) {
    fetch(`cgi-bin/voeg_toe.cgi?language=${language}&start=${start}&end=${end}`)
        .then(antwoord => antwoord.json())
        .then(data => {
            if(data.error){
                alert(data.error);
            } else {
                add_to_tree(data.path);
                outer_update(tree_root);

                $('#searchSelect').append(`<option value="${data.path[0]}">${data.path[0]}</option>`);
                $('#searchSelect').val(data.path[0]).change();
            }
            $("#addButton").attr("disabled", false);
        });
}

function val_or_placeholder(element){
    return $(element).val() || $(element).attr("placeholder");
}

function find_intersection(names){
    let node = tree_root;
    let found;
    names.forEach(name => {
        const children = node.children ?? node._children;
        if (children) {
            found = children.find(child => child.name === name);
            if(found == undefined) return node;
            node = found;
        } else {
            return node;
        }
    });

    return node;
}

function add_to_tree(data) {
    const names = data.slice().reverse();
    let node = find_intersection(names.slice(1));
    if (node.name !== names.slice(-1)[0]) {
        let added = false;
        for(let name of names){
            if(!added){
                if(node.name === name) added = true;

            } else {
                node = create_node(node,name);
            }
        }
    }

}


function create_node(parent,name) {
        if (parent._children != null)  {
            parent.children = parent._children;
            parent._children = null;
        }
        if (parent.children == null) {
            parent.children = [];
        }
        id = crypto.randomUUID(); 
        new_node = { 'name': name, 
                     'id' :  id,
                     'depth': parent.depth + 1,                           
                     'children': [], 
                     '_children':null 
                   };
        console.log('Created Node name: ' + name);
        parent.children.push(new_node);
        return new_node;
}
