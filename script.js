// Functie wordt pas opgeroepen wanneer alle elementen geinitialiseerd zijn.
$('document').ready(function () {

    $("#addButton").click(function () {
        $("#addButton").attr("disabled", true);
        const start = val_or_placeholder("#start_field");
        const end = val_or_placeholder("#end_field");
        const language = val_or_placeholder("#language_field");
        getPath(start, end, language);
    });

    $("#expandButton").click(function () {
        expandAll(tree_root);
        outer_update(tree_root);
    });

    // Een luisteraar dat luistert op veranderingen in taal en doel veld.
    $("#end_field,#language_field").on("change", function () {
        // de tree wordt verwijderd en opnieuw ingesteld met een nieuwe root.
        $("#tree-container").empty();
        draw_tree("",{"name":val_or_placeholder("#end_field")});
        $('#searchSelect').empty();
    });

    
    // Een luisteraar dat luistert op veranderingen in dropdown.
    $('#searchSelect').on('change', function() {
        // Onderstaande functies worden opgeroepen in het d3 script dat ik niet zelf heb geschreven (dndTree.js).
        clearAll(tree_root);
        expandAll(tree_root);
        outer_update(tree_root);

        // Zoekt in de boom
        if (tree_root.children) {
            searchText = $(this).val();
            searchTree(tree_root,true)
            tree_root.children.forEach(collapseAllNotFound);
            outer_update(tree_root);
            tree_root.children.forEach(centerSearchTarget);
        }

    });
    draw_tree("",{"name":val_or_placeholder("#end_field")});
});

/**
* Haalt het pad op uit de databank en voegt deze toe aan de boom.
*/
function getPath(start,end,language) {
    fetch(`cgi-bin/voeg_toe.cgi?language=${language}&start=${start}&end=${end}`)
        .then(antwoord => antwoord.json())
        .then(data => {
            if(data.error){
                // Er is een error object teruggekomen.
                alert(data.error);
            } else {
                add_to_tree(data.path.slice(0,-1).reverse());
                outer_update(tree_root);

                // Voegt de nieuwe start site toe aan de zoeklijst(dropdown).
                $('#searchSelect').append(`<option value="${data.path[0]}">${data.path[0]}</option>`);
                //Roept zelf het verander functie op zodat de nieuwe waarde ingeteld wordt. 
                $('#searchSelect').val(data.path[0]).change();
            }
            $("#addButton").attr("disabled", false);
        });
}

/**
* Haalt waarde op van input veld of indien leeg de placeholder.
*/
function val_or_placeholder(element){
    return $(element).val() || $(element).attr("placeholder");
}


/**
* Voegt de paginas(titels) toe aan boom op de juiste plaats.
*/
function add_to_tree(titles) {
    let node = tree_root;
    let found;
    for(let name of titles){
        const children = node.children ?? node._children ?? [];
        found = children.find(child => child.name === name);
        if(found) {
            node = found;
        } else {
            node = create_node(node,name);
        }
    };
}


/**
* Maakt een nieuwe node aan en voegt het toe aan ouder.
*/
function create_node(parent,name) {
        if (parent._children != null)  {
            parent.children = parent._children;
            parent._children = null;
        }
        if (parent.children == null) {
            parent.children = [];
        }
        // genereert een willekeure id voor de node.
        id = crypto.randomUUID(); 
        new_node = { 'name': name, 
                     'id' :  id,
                     'depth': parent.depth + 1,                           
                     'children': [], 
                     '_children':null 
                   };
        parent.children.push(new_node);

        return new_node;
}
