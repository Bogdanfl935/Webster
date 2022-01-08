namespace exporter.services
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
    using Microsoft.AspNetCore.Mvc;

    public class ParsedImagesService
    {
        internal byte[] ExportImages(string username)
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
            requestParsedImages.AddParameter("username", username);
            requestParsedImages.OnBeforeDeserialization = resp => { resp.ContentType = "application/json"; };
            var responseParsedImages = client.Execute(requestParsedImages);
            var contentParsedImages = responseParsedImages.Content;

            ParsedImagesDto parsedImages = (ParsedImagesDto)JsonConvert.DeserializeObject(contentParsedImages, typeof(ParsedImagesDto));
            List<ParsedImagesDataDto> listOfParsedData = parsedImages.parsedImages;

            string archiveName = username + "_images.zip";

            if (listOfParsedData != null)
            {
                foreach (var element in listOfParsedData)
                {

                    string extension = element.extension;
                    string filename;

                    byte[] valueByte = Convert.FromBase64String(element.content);

                    using (MemoryStream ms = new MemoryStream(valueByte))
                    {
                        using (FileStream zipFile = File.Open(archiveName, FileMode.OpenOrCreate))
                        {
                            Image image = Image.FromStream(ms);
                            filename = "image_" + element.id + "." + extension;

                            using (ZipArchive archive = new ZipArchive(zipFile, ZipArchiveMode.Update))
                            {
                                string source = element.source.Replace("/", "-");
                                ZipArchiveEntry readmeEntry = archive.CreateEntry(source + "/img/" + filename);

                                using (var entryStream = readmeEntry.Open())
                                using (var streamWriter = new StreamWriter(entryStream))
                                using (MemoryStream imageStream = new MemoryStream())
                                {
                                    image.Save(imageStream, dictExtensions[extension]);
                                    streamWriter.Write(imageStream);
                                }
                            }
                        }
                    }
                }
            }
            var myfile = System.IO.File.ReadAllBytes(archiveName);
            return new ExporterContentDto(new FileContentResult(myfile, "application/zip")).encodedFile;
            //return myfile.ToArray();
        }
    }
}