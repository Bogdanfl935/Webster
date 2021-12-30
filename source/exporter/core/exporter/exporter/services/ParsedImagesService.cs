﻿namespace exporter.services
{
    using RestSharp;
    using exporter.constants;
    using exporter.dto;
    using System.Text;
    using Newtonsoft.Json;
    using System.Drawing;
    using System.IO;
    using System.Net;
    using System.Drawing.Imaging;
    using System.IO.Compression;

    public class ParsedImagesService
    {
        internal void ExportImages(int userID)
        {
            var dictExtensions = new Dictionary<string, ImageFormat>()
            {
                {"jpeg", ImageFormat.Jpeg},
                {"jpg", ImageFormat.Jpeg },
                {"png", ImageFormat.Png},
                {"gif", ImageFormat.Gif},
                {"bmp", ImageFormat.Bmp},
                {"ico", ImageFormat.Icon},
                {"exif", ImageFormat.Exif},
                {"tiff", ImageFormat.Tiff},
                {"wmf", ImageFormat.Wmf},
            };

            var nonce = 0;

            var client = new RestClient(AppConstants.appURL + ":" + EndpointConstants.storagePort);


            var requestParsedImages = new RestRequest(EndpointConstants.parsedImageEndpoint, Method.GET);
            requestParsedImages.OnBeforeDeserialization = resp => { resp.ContentType = "application/json"; };
            var responseParsedImages = client.Execute(requestParsedImages);
            var contentParsedImages = responseParsedImages.Content;

            List<Dictionary<string, string>>? listOfDict = JsonConvert.DeserializeObject<List<Dictionary<string, string>>>(contentParsedImages);

            if (listOfDict != null)
            {
                foreach (var dict in listOfDict)
                {
                    string extension = dict[StorageResponseConstants.extensionKey];
                    string filename;

                    byte[] valueByte = Convert.FromBase64String(dict[StorageResponseConstants.contentKey]);

                    using (MemoryStream ms = new MemoryStream(valueByte))
                    {
                        Image image = Image.FromStream(ms);
                        filename = System.Convert.ToBase64String(Encoding.UTF8.GetBytes(extension + nonce + userID)) + userID + "." + extension;
                        image.Save(filename, dictExtensions[extension]);
                        nonce++;
                    }

                    using (FileStream zipFile = File.Open(userID + "_images.zip", FileMode.OpenOrCreate))
                    {
                        using (ZipArchive archive = new ZipArchive(zipFile, ZipArchiveMode.Update))
                        {
                            ZipArchiveEntry readmeEntry = archive.CreateEntry(filename);

                            archive.CreateEntry(filename);
                        }
                    }
                }
            }
        }

        //var results = new ExporterDto(long.Parse(contentNextUrls), long.Parse(contentVisitedUrls));

        //return null;
    }
}