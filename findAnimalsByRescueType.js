function(rescueType) {
    const water_rescue_breeds = ["Labrador Retriever", "Newfoundland", "Chesapeake Bay Retriever", "Turkish Van", "Maine Coon"];
    const mountain_wilderness_breeds = ["German Shepherd", "Border Collie", "Bernese Mountain Dog", "Norwegian Forest Cat", "Siberian Cat"];
    const disaster_tracking_breeds = ["Bloodhound", "Belgian Malinois", "Doberman Pinscher", "Bengal", "Abyssinian"];

    let breeds;
    switch (rescueType) {
        case 'water':
            breeds = water_rescue_breeds;
            break;
        case 'mountain':
            breeds = mountain_wilderness_breeds;
            break;
        case 'disaster':
            breeds = disaster_tracking_breeds;
            break;
        default:
            return []; // Return empty array if type is unknown
    }

    // Return the cursor from the find query, converted to an array
    return db.animals.find({ "breed": { "$in": breeds } }).toArray();
}