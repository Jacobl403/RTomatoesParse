//
// Created by Jacob on 9/4/2025.
//
#include "curl/curl.h"

#include "Requester.h"

#include <iostream>
#include <ostream>

Requester::Requester() {
    init();
}

void Requester::init() {
    CURL * curl = curl_easy_init();
    if (!curl) {
        std::cout << "Curl not initialized" << std::endl;
    }
    std::string url = "https://en.wikipedia.org/wiki/Madame_Web_(film)";
    curl_easy_setopt(curl,CURLOPT_URL,url.c_str());
    curl_easy_setopt(curl,CURLOPT_WRITEFUNCTION,curl_write_callback);
    std::string response;
    curl_easy_setopt(curl,CURLOPT_WRITEDATA,&response);
    std::cout << "ELAGJAK "<< response<< "\n";

}
