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
    //using System.Drawing.Imaging;
    using SixLabors.ImageSharp;
    using System.IO.Compression;
    using Microsoft.AspNetCore.Mvc;
    using SixLabors.ImageSharp.PixelFormats;

    public class ParsedImagesService
    {
        internal byte[] ExportImages(string username)
        {
            var client = new RestClient("http://" + Environment.GetEnvironmentVariable("STORAGE_CONTAINER_NAME") + ":" + EndpointConstants.storagePort);
            //var client = new RestClient("http://127.0.0.1:" + EndpointConstants.storagePort);

            var requestParsedImages = new RestRequest(EndpointConstants.parsedImageEndpoint, Method.GET);
            requestParsedImages.AddParameter("username", username);
            requestParsedImages.OnBeforeDeserialization = resp => { resp.ContentType = "application/json"; };
            var responseParsedImages = client.Execute(requestParsedImages);
            var contentParsedImages = responseParsedImages.Content;

            ParsedImagesDto parsedImages = (ParsedImagesDto)JsonConvert.DeserializeObject(contentParsedImages, typeof(ParsedImagesDto));
            List<ParsedImagesDataDto> listOfParsedData = parsedImages.parsedImages;

            string archiveName = username + "_images.zip";

            if (listOfParsedData != null && listOfParsedData.Count > 0)
            {
                for (var j = 0; j < Math.Min(listOfParsedData.Count, 15); j++)
                {
                    var element = listOfParsedData[j];

                    string extension = element.extension;
                    string filename;

                    byte[] valueByte = Convert.FromBase64String(element.content);

                    using (MemoryStream ms = new MemoryStream(valueByte))
                    {
                        using (FileStream zipFile = File.Open(archiveName, FileMode.OpenOrCreate))
                        {
                            SixLabors.ImageSharp.Formats.IImageFormat format = SixLabors.ImageSharp.Image.DetectFormat(valueByte);
                            SixLabors.ImageSharp.Image image = SixLabors.ImageSharp.Image.Load(valueByte, out format);

                            filename = "image_" + element.id + extension;

                            using (ZipArchive archive = new ZipArchive(zipFile, ZipArchiveMode.Update))
                            {
                                string source = element.source.Replace("/", "-");
                                ZipArchiveEntry readmeEntry = archive.CreateEntry(source + "/img/" + filename);

                                using (var entryStream = readmeEntry.Open())
                                using (var streamWriter = new StreamWriter(entryStream))
                                using (MemoryStream imageStream = new MemoryStream())
                                {
                                    image.Save(imageStream, format);
                                    streamWriter.BaseStream.Write(imageStream.ToArray());
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