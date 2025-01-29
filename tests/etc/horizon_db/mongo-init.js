db = db.getSiblingDB('horizon_db');

const fs = require('fs')
const path = "/data/horizon";

const files = fs.readdirSync(path)

files.forEach(function(file) {
    print('Importing file: ' + file);

    const filePath = path + '/' + file;
    const rawData = JSON.parse(fs.readFileSync(filePath, 'utf8'));

    const convertObjectId = (data) => {
      if (Array.isArray(data)) {
          return data.map(convertObjectId);
      } else if (data && typeof data === 'object') {
          for (let key in data) {
              if (key === '$oid') {
                  return new ObjectId(data[key]);
              } else {
                  data[key] = convertObjectId(data[key]);
              }
          }
      }
      return data;
    };
    const data = convertObjectId(rawData);

    const collectionName = file.split('.')[0];

    db[collectionName].insertMany(data);
    print('Data imported into collection: ' + collectionName);
});
