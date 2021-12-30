# https://hub.docker.com/_/microsoft-dotnet
FROM mcr.microsoft.com/dotnet/sdk:6.0 AS build
WORKDIR /

# copy csproj and restore as distinct layers
COPY *.sln .
COPY exporter/*.csproj ./exporter/

# copy everything else and build app
COPY exporter/. ./exporter/
RUN dotnet publish -c Release -o published

# final stage/image
FROM mcr.microsoft.com/dotnet/aspnet:6.0
COPY  published/. ./published
WORKDIR /published
ENTRYPOINT ["dotnet", "exporter.dll"]