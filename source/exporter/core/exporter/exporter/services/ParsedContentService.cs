namespace exporter.services
{
    using RestSharp;
    using exporter.constants;
    using exporter.dto;
    using System.Text;
    using Newtonsoft.Json;
    using System.IO;
    using System.IO.Compression;
    using Microsoft.AspNetCore.Mvc;
    using SixLabors.ImageSharp;

    public class ParsedContentService
    {
        internal byte[] ExportContent(string username, string url)
        {
            var client = new RestClient("http://" + Environment.GetEnvironmentVariable("STORAGE_CONTAINER_NAME") + ":" + EndpointConstants.storagePort);
            //var client = new RestClient("http://127.0.0.1:" + EndpointConstants.storagePort);


            var requestParsedContent = new RestRequest(EndpointConstants.parsedContentEndpoint, Method.GET);
            requestParsedContent.AddParameter("username", username);
            requestParsedContent.AddParameter("source", url);
            requestParsedContent.OnBeforeDeserialization = resp => { resp.ContentType = "application/json"; };
            var responseParsedContent = client.Execute(requestParsedContent);
            var contentParsedContent = responseParsedContent.Content;

            ParsedContentDto parsedContent = (ParsedContentDto)JsonConvert.DeserializeObject(contentParsedContent, typeof(ParsedContentDto));
            List<ParsedContentDataDto> listOfParsedData = parsedContent.parsedContent;

            string archiveName = username + "_content.zip";

            if (listOfParsedData != null && listOfParsedData.Count > 0)
            {
                for (var i = 0;i < listOfParsedData.Count; i ++)
                {
                    var element = listOfParsedData[i];
                    string filename;

                    byte[] valueByte = Convert.FromBase64String(element.content);


                    using (MemoryStream ms = new MemoryStream(valueByte))
                    {
                        using (FileStream zipFile = File.Open(archiveName, FileMode.OpenOrCreate))
                        {
                            filename = element.tag + "_" + element.id + ".txt";

                            using (ZipArchive archive = new ZipArchive(zipFile, ZipArchiveMode.Update))
                            {
                                string source = element.source.Replace("/", "-");
                                ZipArchiveEntry readmeEntry = archive.CreateEntry(source + "/" + element.tag + "/" + filename);

                                using (var entryStream = readmeEntry.Open())
                                using (var streamWriter = new StreamWriter(entryStream, Encoding.UTF8))
                                {
                                    streamWriter.BaseStream.Write(valueByte, 0, valueByte.Length);
                                }
                            }
                        }
                    }
                }
            }


            var requestParsedImages = new RestRequest(EndpointConstants.parsedImageEndpoint, Method.GET);
            requestParsedImages.AddParameter("username", username);
            requestParsedImages.AddParameter("source", url);
            requestParsedImages.OnBeforeDeserialization = resp => { resp.ContentType = "application/json"; };
            var responseParsedImages = client.Execute(requestParsedImages);
            var contentParsedImages = responseParsedImages.Content;

            ParsedImagesDto parsedImages = (ParsedImagesDto)JsonConvert.DeserializeObject(contentParsedImages, typeof(ParsedImagesDto));
            List<ParsedImagesDataDto> listOfParsedImagesData = parsedImages.parsedImages;

            var imageWriter = new ParsedImagesService();
            imageWriter.ExportImages(listOfParsedImagesData, archiveName);

            var myfile = System.IO.File.ReadAllBytes(archiveName);
            return new ExporterContentDto(new FileContentResult(myfile, "application/zip")).encodedFile;
            //return new ExporterContentDto(myfile).encodedFile;
        }
    }
}

